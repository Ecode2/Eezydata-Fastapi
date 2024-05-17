"""Bills Payment related endpoints."""
import logging
from typing import Annotated, List
from fastapi import Body, Depends, HTTPException, Query, status, APIRouter
from app.db.models.auth import AuthUser
from app.db.models.ebills import History
from app.db.models.paystack import Wallet
from app.db.queries.bills import get_plan
from app.db.session import session_scope
from app.schemas.auth import AuthUserPublic
from app.schemas.bills import BillsModel, PriceModel, PriceUpdate, PricesPublic
from app.services.bill_funcs import get_bill_balance, pay_airtime_bill, pay_cable_bill, pay_data_bill, pay_electric_bill
from app.services.paystack_funcs import paystack_balance
from app.utils.storage import store_price, store_record, update_price, update_user
from ebills.models.verify import VerifyModel, VerifyResponse
from ebills import Verify
from ....utils.security import (get_current_active_user, get_super_user, http_auth)
from ....configs import get_settings

 
settings = get_settings()
bill_router = APIRouter()
logger = logging.getLogger(settings.PROJECT_SLUG)

@bill_router.post("/electric/verify",
                  dependencies=[Depends(http_auth)],
                  response_model=VerifyResponse,)
async def verify_electricity(Info: VerifyModel, current_user: AuthUserPublic = Depends(get_current_active_user)):
    """Verify users electricity account identity

    \f

    Args:
        Info: (VerifyModel): model of the required info containing
            customer_id: (str) _meter number length of 11 numbers_
            service_id: (str) _meter number acount type_ 
                [ abuja-electric , eko-electric , ibadan-electric , ikeja-electric , 
                jos-electric , kaduna-electric , kano-electric , portharcout-electric ]
            variation_id: Optional[str]. _Type of electric bill _
                [ prepaid ,  postpaid ]
        current_user (:obj:`..schemas.auth.User`): the corresponding user of the
          pass token.

    Returns:
        VerifyResponse: All information about meter number account.
        400 Bad Request error : if parameters are not complete

    """

    try:
        verify_info = await Verify.verify(Info.dict())
        return verify_info
    except Exception as e:
        msg = f"Error [{e}] occured while verifying account at elecrtic/verify."
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Information inaccurate error {e}")
    

@bill_router.post("/cable/verify",
                  dependencies=[Depends(http_auth)],
                  response_model=VerifyResponse,)
async def verify_cable(Info: VerifyModel, current_user: AuthUserPublic = Depends(get_current_active_user)):
    """Verify users cable tv account identity

    \f

    Args:
        Info: (VerifyModel): model of the required info containing
            customer_id: (str) _smartcard number length of 10 numbers_
            service_id: (str) _smartcard number acount type_ 
                [ dstv , gotv , startimes ]
        current_user (:obj:`..schemas.auth.User`): the corresponding user of the
          pass token.

    Returns:
        VerifyResponse: All information about meter number account.
        400 Bad Request error : if parameters are not complete

    """
    try:
        verify_info = await Verify.verify(Info.dict())
        return verify_info
    except Exception as e:
        msg = f"Error [{e}] occured while verifying account at cable/verify."
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Information inaccurate error {e}")

@bill_router.post("/plan",
                  tags=["Price"],
                  #response_model=List[PricesPublic],
                  dependencies=[Depends(http_auth)]
                  ) 
async def get_available_plan(bill_form:PriceModel = Body(None), current_user: AuthUserPublic = Depends(get_current_active_user)):
    """Get bill prices according to request

    \f

    Args:
        bill_form: (PriceModel): model of the required info containing
            bill_type: (str) the bill like cable
            brand: (str) the bill brand like [ dstv , gotv , startimes ]

    Returns:
        [PricesPublic]: All information about meter number account.
        400 Bad Request error : if parameters are not complete

    """
    try:
        get_price_info = get_plan(**bill_form.model_dump())
        if type(get_price_info) is list:
            return get_price_info
        
        if get_price_info is not False:
            return [get_price_info]
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Prices could not be found")
        
    except Exception as e:
        msg = "Error [{}] occured while getting {} price.".format(e, bill_form.brand)
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Information inaccurate error {e}")
    
@bill_router.post("/plan/add",
                  tags=["Admin", "Price"],
                  response_model=PricesPublic,
                  dependencies=[Depends(http_auth)]
                  ) 
async def add_billing_plan(bill_form:PricesPublic = Body(None), current_user: AuthUserPublic = Depends(get_super_user)):
    """Add bill price according to request

    \f

    Args:
        bill_form: (PriceModel): model of the required info containing
        bill_type: (str) the bill like cable
        brand: (str) the bill brand like [ dstv , gotv , startimes ]
        code: (str) the bill code like [ nova , basic , smart ]

    Returns:
        [PricesPublic]: All information about meter number account.
        400 Bad Request error : if parameters are not complete

    """
    try:
        add_new_price = store_price(**bill_form.model_dump(), is_superuser=current_user.is_superuser)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to store in DB. error {e}")
    if not add_new_price:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Bill already exists.")
    
    return add_new_price

@bill_router.put("/plan/update",
                  tags=["Admin", "Price"],
                  response_model=PricesPublic,
                  dependencies=[Depends(http_auth)]
                  ) 
async def update_billing_plan(bill_form:PriceModel = Body(None), bill_update: PriceUpdate = Body(None), current_user: AuthUserPublic = Depends(get_super_user)):
    """Update bill price according to request

    \f

    Args:
        bill_form: (PriceModel): model of the required info containing
        bill_type: (str) the bill like cable
        brand: (str) the bill brand like [ dstv , gotv , startimes ]
        code: (str) the bill code like [ nova , basic , smart ]
        price: (str) the bill price

    Returns:
        [PricesPublic]: All information about meter number account.
        400 Bad Request error : if parameters are not complete

    """
    try:
        change_price = update_price(old_bill_type=bill_form.bill_type, old_brand=bill_form.brand, old_code=bill_form.code, is_superuser=current_user.is_superuser, **bill_update.model_dump())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to update store in DB. error {e}")
    if not change_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Admin privelages required.")
    
    return change_price


@bill_router.post("/data",
                  dependencies=[Depends(http_auth)]
                  )
async def buy_data_subscription(bill_form:BillsModel = Body(None), current_user: AuthUserPublic = Depends(get_current_active_user)):

    with session_scope() as session:

        active_user = AuthUser.get_user(db_session=session, username=current_user.username )
        bill_form.user_id = active_user.get("id")

        if current_user.wallet_type == "paystack":

            wallet_info = Wallet.get_wallet(db_session=session, authUser_id=bill_form.user_id, populate=True)
            bill_form.wallet_id = wallet_info.user_code

            ebill_balance = get_bill_balance()
            if ebill_balance == None:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=f"Bill API is currently unavailable")
            
            if ebill_balance <= bill_form.amount:
                #TODO: make paystack transactions here
                pass
            
            if current_user.balance < bill_form.amount:
                raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,
                            detail=f"Balance too low for purchase") 
            
            try:
                bill_payment = pay_data_bill(phone=bill_form.phone, network=bill_form.brand,
                                            code=bill_form.code, user_id=bill_form.user_id,
                                            wallet_id=bill_form.wallet_id)
                
                record = store_record(authUser_id=bill_form.user_id, wallet_id=bill_form.wallet_id,
                                    order_id=bill_payment.order_id, status= bill_payment.code,
                                    message=bill_payment.message, bill_type=bill_form.bill_type,
                                    brand=bill_payment.network, name=bill_form.name,
                                    code=bill_form.code, price=bill_payment.amount)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occured while making payment {e}") 

            update_user(user=current_user.username, balance=current_user.balance - bill_form.amount )

            if paystack_balance() > bill_form.amount and ebill_balance > bill_form.amount:

                #TODO: then innitiate paystack back function transfer with history id to update 
                # => transaction_id in history table 
                pass

            return record

        elif current_user.wallet_type == "monify":
            pass


@bill_router.post("/airtime",
                  dependencies=[Depends(http_auth)]
                  )
async def buy_airtime(bill_form:BillsModel = Body(None), current_user: AuthUserPublic = Depends(get_current_active_user)):
    
    with session_scope() as session:

        active_user = AuthUser.get_user(db_session=session, username=current_user.username )
        bill_form.user_id = active_user.get("id")

        if current_user.wallet_type == "paystack":

            wallet_info = Wallet.get_wallet(db_session=session, authUser_id=bill_form.user_id, populate=True)
            bill_form.wallet_id = wallet_info.user_code

            ebill_balance = get_bill_balance()
            if ebill_balance == None:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=f"Bill API is currently unavailable")
            
            if ebill_balance <= bill_form.amount:
                #TODO: make paystack transactions here
                pass
            
            if current_user.balance < bill_form.amount:
                raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,
                            detail=f"Balance too low for purchase") 
            
            try:
                bill_payment = pay_airtime_bill(phone=bill_form.phone, network=bill_form.brand,
                                            amount=bill_form.amount, user_id=bill_form.user_id,
                                            wallet_id=bill_form.wallet_id)
                
                record = store_record(authUser_id=bill_form.user_id, wallet_id=bill_form.wallet_id,
                                    order_id=bill_payment.order_id, status= bill_payment.code,
                                    message=bill_payment.message, bill_type=bill_form.bill_type,
                                    brand=bill_payment.network, name=bill_form.name,
                                    code=bill_form.code, price=bill_payment.amount)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occured while making payment {e}") 

            update_user(user=current_user.username, balance=current_user.balance - bill_form.amount )
            

            if paystack_balance() > bill_form.amount and ebill_balance > bill_form.amount:

                #TODO: then innitiate paystack back function transfer with history id to update 
                # => transaction_id in history table 
                pass

            return record

        elif current_user.wallet_type == "monify":
            pass


@bill_router.post("/cable",
                  dependencies=[Depends(http_auth)]
                  )
async def buy_cable_tv(bill_form:BillsModel = Body(None), current_user: AuthUserPublic = Depends(get_current_active_user)):
    
    with session_scope() as session:

        active_user = AuthUser.get_user(db_session=session, username=current_user.username )
        bill_form.user_id = active_user.get("id")

        if current_user.wallet_type == "paystack":

            wallet_info = Wallet.get_wallet(db_session=session, authUser_id=bill_form.user_id, populate=True)
            bill_form.wallet_id = wallet_info.user_code

            ebill_balance = get_bill_balance()
            if ebill_balance == None:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=f"Bill API is currently unavailable")
            
            if not bill_form.amount:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Price required")
            
            if ebill_balance <= bill_form.amount:
                #TODO: make paystack transactions here
                pass
            
            if current_user.balance < bill_form.amount:
                raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,
                            detail=f"Balance too low for purchase") 
            
            try:
                bill_payment = pay_cable_bill(phone=bill_form.phone, service=bill_form.brand,
                                            variation=bill_form.code, user_id=bill_form.user_id,
                                            smartcard= bill_form.smartcard, wallet_id=bill_form.wallet_id)
                
                record = store_record(authUser_id=bill_form.user_id, wallet_id=bill_form.wallet_id,
                                    order_id=bill_payment.order_id, status= bill_payment.code,
                                    message=bill_payment.message, bill_type=bill_form.bill_type,
                                    brand=bill_form.brand, name=bill_form.name,
                                    code=bill_form.code, price=bill_payment.amount)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occured while making payment {e}") 

            update_user(user=current_user.username, balance=current_user.balance - bill_form.amount )
            

            if paystack_balance() > bill_form.amount and ebill_balance > bill_form.amount:

                #TODO: then innitiate paystack back function transfer with history id to update 
                # => transaction_id in history table 
                pass

            # TODO: return a custom model for cale purchase
            # => with record and bill_payment together
            return record

        elif current_user.wallet_type == "monify":
            pass


@bill_router.post("/electric",
                  dependencies=[Depends(http_auth)]
                  )
async def buy_electric_token(bill_form:BillsModel = Body(None), current_user: AuthUserPublic = Depends(get_current_active_user)):
    
    with session_scope() as session:

        active_user = AuthUser.get_user(db_session=session, username=current_user.username )
        bill_form.user_id = active_user.get("id")

        if current_user.wallet_type == "paystack":

            wallet_info = Wallet.get_wallet(db_session=session, authUser_id=bill_form.user_id, populate=True)
            bill_form.wallet_id = wallet_info.user_code

            ebill_balance = get_bill_balance()
            if ebill_balance == None:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=f"Bill API is currently unavailable")
            
            if not bill_form.amount:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Price required")
            
            if ebill_balance <= bill_form.amount:
                #TODO: make paystack transactions here
                pass
            
            if current_user.balance < bill_form.amount:
                raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,
                            detail=f"Balance too low for purchase") 
            
            try:
                bill_payment = pay_electric_bill(phone=bill_form.phone, service=bill_form.brand,
                                            variation=bill_form.code, user_id=bill_form.user_id,
                                            meter= bill_form.meter, wallet_id=bill_form.wallet_id,
                                            amount=int(bill_form.amount))
                
                record = store_record(authUser_id=bill_form.user_id, wallet_id=bill_form.wallet_id,
                                    order_id=bill_payment.order_id, status= bill_payment.code,
                                    message=bill_payment.message, bill_type=bill_form.bill_type,
                                    brand=bill_form.brand, name=bill_form.name,
                                    code=bill_form.code, price=bill_payment.amount)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occured while making payment {e}") 

            update_user(user=current_user.username, balance=current_user.balance - bill_form.amount )
            

            if paystack_balance() > bill_form.amount and ebill_balance > bill_form.amount:

                #TODO: then innitiate paystack back function transfer with history id to update 
                # => transaction_id in history table 
                pass

            # TODO: return a custom model for electricity purchase
            # => with record and bill_payment together
            return bill_payment

        elif current_user.wallet_type == "monify":
            pass

#TODO: Endpoint to make payment according to the user bank

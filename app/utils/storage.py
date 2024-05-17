"""Define functions for storing information to storage."""
# mypy: ignore-errors
import logging
from typing import Any
from app.db.models.ebills import History, Prices
from app.schemas.bills import PricesPublic, RecordsPublic
from app.schemas.paystack import PaystackPublic
from ..db.models import AuthUser, Wallet
from ..db.session import session_scope
from ..schemas.auth import AuthUserPublic
from ..configs import get_settings

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)

# Authentication
def store_user(username: str, password: str, firstname: str,
               lastname: str, email: str, phone: str,
               is_superuser: bool = False, raw: bool = False):
    """Create new user and store it in DB.

    Args:
        username (str): username.
        password (str): plaintext password.
        firstname (str): first name of the user.
        lastname (str): last name of the user.
        phone (str): phone number of the user.
        email (str): email of the user.
        is_superuser (bool, optional): the user will be a superuser.
        raw (bool, optional): returns the unprocess sqlalchemy response if true.

    Returns:
        AuthUserPublic: stored user's account information.
    """
    with session_scope() as session:
        user_exists = session.query(AuthUser).filter(
            AuthUser.username == username).scalar()
        if user_exists:
            msg = f"Username [{username}] is used already."
            logger.error(msg)
            return None
        
        user = AuthUser.create_user(username=username,
                                    password=password,
                                    firstname=firstname,
                                    lastname=lastname,
                                    email=email,
                                    phone=phone,
                                    is_superuser=is_superuser)
        session.add(user)
        session.commit()
        msg = f"Successfully stored AuthUser[id=\"{user.id}\", username=\"{username}\"]"
        logger.info(msg)
        if raw:
            return user._asdict()
        
        return AuthUserPublic(**user._asdict())

def update_user(user: str, secret:str = "", **kwargs):
    """Update user info and store it in DB.

    Args:
        user (str): username.
        secret (str, optional): plaintext password required for username and password update.
        kwargs (dict): name arguments of information to be updates.

    Returns:
        AuthUserPublic: stored user's account information.
    """

    with session_scope() as session:
        user_info = AuthUser.get_user(db_session=session, username=user)

        #session.add(user_info)
        logger.info(msg=[user_info.id, kwargs])
    
        for k, v in kwargs.items():

            if v and k == "password":

                if not AuthUser.authenticate_user(username=user, password=secret):
                    msg = f"Username or password is incorrect."
                    logger.error(msg)
    
                    return False
                
                session.query(AuthUser).filter(AuthUser.username == user).update({k: AuthUser.get_password_hash(v) }, synchronize_session='evaluate' )
                session.commit()
                continue

            if v and k == "username":

                if not AuthUser.authenticate_user(username=user, password=secret):
                    msg = f"Username or password is incorrect."
                    logger.error(msg)
    
                    return False
                
                session.query(AuthUser).filter(AuthUser.username == user).update({k: v }, synchronize_session='evaluate' )
                session.commit()
                print(f"{k} updated")
                continue

            if v:
                session.query(AuthUser).filter(AuthUser.username == user).update({k:v}, synchronize_session='evaluate' )
                session.commit()

            
        msg = f"Successfully updated AuthUser[id=\"{user_info.id}\", username=\"{user}\"]"
        logger.info(msg)
        return AuthUserPublic(**user_info._asdict())
    

# Wallet
def store_customer(id: int, authUser_id: str,
                   customer_code: str, integration: int, 
                    is_superuser: bool = False, raw: bool = False):
    """Create new user and store it in DB.

    Args:
        id (int): customer id of paystack.
        authUser_id (str): uuid of the current user.
        customer_code (str): customer code of paystack.
        integration (int): integration number of the paystack customer.
        raw (bool): Returns non parased wallet info if true
        is_superuser (bool, optional): the user will be a superuser.

    Returns:
        PaystackPublic: stored user's account information.
    """
    with session_scope() as session:
        wallet_exists = session.query(Wallet).filter(
            Wallet.authUser_id == authUser_id).scalar()
        if wallet_exists:
            msg = f"Username with id [{authUser_id}] is used already."
            logger.error(msg)
            return None
        
        new_wallet = Wallet.create_wallet(authUser_id=authUser_id,
                                    user_id=id,
                                    user_code= customer_code,
                                    integration= integration)
        session.add(new_wallet)
        session.commit()

        
        user = AuthUser.get_user(db_session=session, user_id=authUser_id, populate=True)
        update_user(user=user.username, wallet_type="paystack")

        msg = f"Successfully stored Wallet[id=\"{new_wallet.id}\", user code =\"{new_wallet.user_code}\"]"
        logger.info(msg)

        if raw:
            return new_wallet._asdict()
        
        return PaystackPublic(**new_wallet._asdict())

#TODO: create update customer to add virtual account info

#Bill prices
def store_price(bill_type: str, brand: str, name: str,
               code: str, price: str, is_superuser: bool = False, 
               raw: bool = False)-> Any:
    """Create new bill price and store it in DB.

    Args:
        bill_type (str): type of bill like [data, airtime, cable, electric]
        brand (str): chosen bill brand [mtn, glo, airtel, 9moile]
        name (str): Bills name 
        code (str): unique code identifier
        price (dict): the cost of the bill
        is_superuser (bool, optional): the user must be a superuser.
        raw (bool, optional): returns the unprocess sqlalchemy response if true.

    Returns:
        PricePublic: stored user's account information.
    """

    # Stop if user doesn't have privelages
    if not is_superuser or not bill_type and not brand and not code and not name:
        return None

    with session_scope() as session:
        price_exists = session.query(Prices).filter_by(bill_type = bill_type, brand=brand, code=code).scalar()
        if price_exists:
            msg = f"Bill of code [{code}] is already registered."
            logger.error(msg)
            return None
        
        price = Prices.add_price(bill_type=bill_type, 
                                brand=brand,
                                name=name, 
                                code=code,
                                price=price)
        session.add(price)
        session.commit()
        msg = f"Successfully stored Bill Price[name=\"{price.name}\", code=\"{price.code}\"]"
        logger.info(msg)
        if raw:
            return price._asdict()
        
        return PricesPublic(**price._asdict())
    
def update_price(old_bill_type: str, old_brand:str, old_code:str,
                 is_superuser: bool = False, raw: bool = False, **kwargs):
    """Update price info and store it in DB.

    Args:
        bill_type (str): type of bill like [data, airtime, cable, electric]
        brand (str): bill brand [mtn, glo, airtel, 9moile]
        code (str): bill brand code
        kwargs (dict): name arguments of information to be updates.

    Returns:
        PricePublic: stored price information.
    """
    if not is_superuser or not old_bill_type and not old_brand and not old_code:
        return None

    with session_scope() as session:
        price_info = Prices.get_prices(db_session=session, bill_type=old_bill_type, brand=old_brand, code=old_code)

        logger.info(msg=[price_info, kwargs])
    
        for k, v in kwargs.items():

            if v:
                session.query(Prices).filter_by(bill_type = old_bill_type, brand=old_brand, code=old_code).update({k:v}, synchronize_session='evaluate' )
                session.commit()
                logger.info(msg=f"{k} updated")

                
        msg = f"Successfully updated prices with [code=\"{price_info.code}\" and brand=\"{old_brand}\"]"
        logger.info(msg)

        if raw:
            return price_info._asdict()
        
        return PricesPublic(**price_info._asdict())
    
    
#Bill history
def store_record(authUser_id: str, wallet_id: str,
                 order_id: str, status: str,
                 transaction_id: str = None, raw: bool = False, 
                 **kwargs):
    """Create new history record and store it in DB.

    Args:
        transaction_id (str): od of the wallet transaction.
        authUser_id (str): uuid of the current user.
        wallet_id (str): wallet id of paystack Wallet table.
        orde_id (str): orde_id of the bill transaction.
        status (str): status code of the bill transaction [success, failure]
        kwargs (dict): other user information.
        raw (bool, optional): returns the unprocess sqlalchemy response if true.

    Returns:
        RecordsPublic: stored new history record.
    """
    with session_scope() as session:
        record_exists = session.query(History).filter(
            History.order_id == order_id).scalar()
        """ if record_exists:
            msg = f"Record with order id [{order_id}] exists."
            logger.error(msg)
            return None """
        
        new_record = History.create_new_record(transaction_id=transaction_id,
                                        authUser_id=authUser_id,
                                        wallet_id=wallet_id,
                                        order_id=order_id,
                                        status=status,
                                        **kwargs)
        
        session.add(new_record)
        session.commit()
        msg = f"Successfully stored History[id=\"{order_id}\", wallet id=\"{wallet_id}\"]"
        logger.info(msg)

        if raw:
            return new_record._asdict()
        
        return RecordsPublic(**new_record._asdict())

#TODO: function to update a record with specific order id and authuser id
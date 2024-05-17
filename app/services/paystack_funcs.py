"""Create all paystack integrations"""
from app.schemas.auth import AuthUserPublic
from app.schemas.paystack import PaystackCreate
from paystack import Customer, Balance
from ..utils.storage import store_customer
from ..db.models import Wallet
from ..configs import get_settings
from ..db.session import session_scope
from json import dumps
import paystack, os, logging
from dotenv import load_dotenv

load_dotenv(override=True)

paystack.api_key = os.getenv("API_AUTH_KEY")
settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


def paystack_create_user(authUser: dict):
    authUser_id = authUser.get("id")

    
    customer = Customer.create(
        email= authUser.get("email"),
        first_name=authUser.get("firstname"),
        last_name= authUser.get("lastname"),
        phone= "+234{}".format(authUser.get("phone")[1:] ),
        metadata= {"picture": authUser.get("picture"), "authUser_id": authUser.get("id"),}
        ) 
    
    dict_customer = customer.to_dict()
    dict_customer["data"]["authUser_id"] = authUser_id
    
    store_customer( **PaystackCreate( **dict_customer["data"]).model_dump() , raw=True)

    # TODO: create dedicated virtual account


def paystack_virtual_account():
    pass


def paystack_balance()-> None | int:

    response = Balance.fetch()
    response = response.to_dict()
    

    """ try:
        response = Balance.fetch()
        if response.code != "success":
            print(response)
            return None
        
        print(response)
        return int(response.balance)
    except Exception as e:
        print(e)
        return None """

def paystack_transfer(bill, current_user:AuthUserPublic ):

    balance = current_user.balance
    


#TODO: write a function to initiate a transfer from my paystack account
# => to the ebills account but it will start with checking user balance from
# => authUser table if it is enough if it is then it will create a new thread to 
# => initiate and finalise the transfer from paystack to the ebiils app while 
# => continuing the bill payment in the main thread if the ebill balance is enough
# => when the bill has been successfully bought it will then subtract the balance from the 
# => authUser table, and 
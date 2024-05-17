"""Define functions for all bill related endpoints"""
# mypy: ignore-errors
import logging, ebills, os, logging
from typing import Any
from app.db.models.ebills import Prices
from app.schemas.bills import PricesPublic
from ebills.models import DataResponse, AirtimeResponse, ElectricResponse, CableResponse
from ..configs import get_settings
from ebills import Balance, Data, Airtime, Electricity, Cable
from dotenv import load_dotenv

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)

load_dotenv(override=True)

ebills.username = os.getenv("EBILLS_USERNAME")
ebills.password = os.getenv("EBILLS_PASSWORD")


def get_bill_balance()-> None | int:
    try:
        response = Balance.check()
        if response.code != "success":
            print(response)
            return None
        
        print(response)
        return int(response.balance)
    except Exception as e:
        print(e)
        return None
    
def pay_data_bill(phone:str, network:str, code:str, **kwargs) -> None | DataResponse:

    if not kwargs.get("user_id") and kwargs.get("wallet id"):
        return None
    
    try:
        parameters= {
            "phone": phone,
            "network_id": network,
            "variation_id": code
        }
        response = Data.buy(parameters=parameters)

        if response.code != "success":
            print(response)
            #TODO: save failed transfer with response.order_id to bill History table
            return None
        
        print(response)
        #TODO: save successful transfer with response.order_id and user_id and wallet id to bill History table
        return response
    
    except Exception as e:
        print(e)
        #TODO: save failed transfer with response.order_id to bill History table
        return None
    
def pay_airtime_bill(phone:str, network:str, amount:int, **kwargs) -> None | AirtimeResponse:

    if not kwargs.get("user_id") and kwargs.get("wallet id"):
        return None
    
    try:
        parameters= {
            "phone": phone,
            "network_id": network,
            "amount": int(amount)
        }
        response = Airtime.buy(parameters=parameters)

        if response.code != "success":
            print(response)
            #TODO: save failed transfer with response.order_id to bill History table
            return None
        
        print(response)
        #TODO: save successful transfer with response.order_id and user_id and wallet id to bill History table
        return response
    
    except Exception as e:
        print(e)
        #TODO: save failed transfer with response.order_id to bill History table
        return None

def pay_electric_bill(phone:str, service:str, variation:str, meter:str,  amount:int, **kwargs) -> None | ElectricResponse:

    if not kwargs.get("user_id") and kwargs.get("wallet id"):
        return None
    
    try:
        parameters= {
            "phone": phone,
            "service_id": service,
            "meter_number": meter,
            "variation_id": variation,
            "amount": int(amount)
        }
        response = Electricity.buy(parameters=parameters)

        if response.code != "success":
            print(response)
            #TODO: save failed transfer with response.order_id to bill History table
            return None
        
        print(response)
        #TODO: save successful transfer with response.order_id and user_id and wallet id to bill History table
        return response
    
    except Exception as e:
        print(e)
        #TODO: save failed transfer with response.order_id to bill History table
        return None

def pay_cable_bill(phone:str, service:str, variation:str, smartcard:str,  **kwargs) -> None | CableResponse:

    if not kwargs.get("user_id") and kwargs.get("wallet id"):
        return None
    
    try:
        parameters= {
            "phone": phone,
            "service_id": service,
            "smartcard_number": smartcard,
            "variation_id": variation
        }
        response = Cable.buy(parameters=parameters)

        if response.code != "success":
            print(response)
            #TODO: save failed transfer with response.order_id to bill History table
            return None
        
        print(response)
        #TODO: save successful transfer with response.order_id and user_id and wallet id to bill History table
        return response
    
    except Exception as e:
        print(e)
        #TODO: save failed transfer with response.order_id to bill History table
        return None
from pydantic import BaseModel, constr, field_validator
from typing import Optional, List


class DataModel(BaseModel):
    phone: constr(strip_whitespace=True, min_length=11, max_length=11) # type: ignore
    network_id: constr(
        strip_whitespace=True, 
        pattern=r"^(mtn|glo|airtel|etisalat)$"
        ) # type: ignore
    variation_id: constr(
        strip_whitespace=True, 
        pattern=r"^(500|M1024|M2024|3000|5000|10000|mtn-20hrs-1500|mtn-30gb-8000|mtn-40gb-10000|mtn-75gb-15000|glo100x|glo200x|G500|G2000|G1000|G2500|G3000|G4000|G5000|G8000|glo10000|airt-1100|airt-1300|airt-1650|airt-2200|airt-3300|airt-5500|airt-11000|airt-330x|airt-550|airt-500x|airt-1650-2|9MOB1000|9MOB34500|9MOB8000|9MOB5000)$"
        ) # type: ignore
    
    @field_validator('network_id')
    def check_network_id(cls, v):
        if v not in ["mtn", "glo", "airtel", "etisalat"]:
            raise ValueError("Network id is not recognised")
        return v
    
    @field_validator('variation_id')
    def check_variation_id(cls, v):
        if v not in ["500","M1024","M2024","3000","5000","10000","mtn-20hrs-1500","mtn-30gb-8000","mtn-40gb-10000","mtn-75gb-15000","glo100x","glo200x","G500","G2000","G1000","G2500","G3000","G4000","G5000","G8000","glo10000","airt-1100","airt-1300","airt-1650","airt-2200","airt-3300","airt-5500","airt-11000","airt-330x","airt-550","airt-500x","airt-1650-2","9MOB1000","9MOB34500","9MOB8000","9MOB5000"]:
            raise ValueError("Variation id is not recognised")
        return v

    @field_validator('phone')
    def check_phone(cls, v):
        if len(v) != 11 :
            raise ValueError("Phone number is not complete")
        return v

class DataResponse(BaseModel):
    code: Optional[str]
    message: Optional[str]
    network: Optional[str]
    data_plan: Optional[str]
    phone: Optional[str]
    amount: Optional[str]
    order_id: Optional[str]
    
    @classmethod
    def get_info(cls, data: dict):
        if data.get("code") == "success":
            return cls(
                code=data.get('code'),
                message=data.get('message'),
                network=data['data'].get('network'),
                data_plan=data['data'].get('data_plan'),
                phone=data['data'].get('phone'),
                amount=data['data'].get('amount'),
                order_id=data['data'].get('order_id')
            )
        elif data.get("code") == "failure":
            return cls(
                code=data.get('code'),
                message=data.get('message'),
                order_id=data.get('order_id')
            )
        else:
            raise ValueError("Invalid or unknown data passed ")
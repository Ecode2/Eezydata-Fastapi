from pydantic import BaseModel, constr, field_validator
from typing import Optional

class AirtimeModel(BaseModel):
    phone: constr(strip_whitespace=True, min_length=11, max_length=11) # type: ignore
    network_id: constr(
        strip_whitespace=True, 
        pattern=r"^(mtn|glo|airtel|etisalat)$"
        ) # type: ignore
    amount: int

    @field_validator('network_id')
    def check_network_id(cls, v):
        if v not in ["mtn", "glo", "airtel", "etisalat"]:
            raise ValueError("Network id is not recognised")
        return v
    
    @field_validator('phone')
    def check_phone(cls, v):
        if len(v) != 11 :
            raise ValueError("Phone number is not complete")
        return v

class AirtimeResponse(BaseModel):
    code: Optional[str]
    message: Optional[str]
    network: Optional[str]
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
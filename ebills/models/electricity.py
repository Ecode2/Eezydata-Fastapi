from pydantic import BaseModel, constr, field_validator
from typing import Optional, List



class ElectricModel(BaseModel):
    phone: constr(strip_whitespace=True, min_length=11, max_length=11) # type: ignore
    service_id: constr(
        strip_whitespace=True, 
        pattern=r"^(abuja-electric|eko-electric|ibadan-electric|ikeja-electric|jos-electric|kaduna-electric|kano-electric|portharcout-electric)$"
        ) # type: ignore 
    variation_id: constr(
        strip_whitespace=True, 
        pattern=r"^(prepaid|postpaid)$"
        ) # type: ignore
    meter_number: constr(strip_whitespace=True, min_length=11, max_length=11) # type: ignore
    amount: int
    
    @field_validator('phone')
    def check_phone(cls, v):
        if len(v) != 11 :
            raise ValueError("Phone number is not complete")
        return v
    
    @field_validator('meter_number')
    def check_meter_number(cls, v):
        if len(v) != 11 :
            raise ValueError("Meter_number number is not complete")
        return v
    
    @field_validator('service_id')
    def check_service_id(cls, v):
        if v not in ["abuja-electric","eko-electric","ibadan-electric","ikeja-electric","jos-electric","kaduna-electric","kano-electric","portharcout-electric"]:
            raise ValueError("Service id is not recognised")
        return v
    
    @field_validator('variation_id')
    def check_variation_id(cls, v):
        if v not in ["prepaid", "postpaid"]:
            raise ValueError("Variation id is not recognised")
        return v
    

class ElectricResponse(BaseModel):
    code: Optional[str]
    message: Optional[str]
    electricity: Optional[str]
    meter_number: Optional[str]
    token: Optional[str]
    units: Optional[str]
    phone: Optional[str]
    amount: Optional[str]
    amount_charged: Optional[str]
    order_id: Optional[str]

    @classmethod
    def get_info(cls, data: dict):
        if data.get("code") == "success":
            return cls(
                code=data.get('code'),
                message=data.get('message'),
                electricity=data['data'].get('electricity'),
                meter_number=data['data'].get('meter_number'),
                token=data['data'].get('token'),
                units=data['data'].get('units'),
                phone=data['data'].get('phone'),
                amount=data['data'].get('amount'),
                amount_charged=data['data'].get('amount_charged'),
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
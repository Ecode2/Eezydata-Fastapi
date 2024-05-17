from pydantic import BaseModel, constr, field_validator
from typing import Optional, List


class VerifyModel(BaseModel):
    customer_id: constr(strip_whitespace=True, min_length=10, max_length=11) # type: ignore
    service_id: constr(
        strip_whitespace=True, 
        pattern=r"^(dstv|gotv|startimes|abuja-electric|eko-electric|ibadan-electric|ikeja-electric|jos-electric|kaduna-electric|kano-electric|portharcout-electric)$"
        ) # type: ignore
    variation_id: Optional[constr(
        strip_whitespace=True, 
        pattern=r"^(prepaid|postpaid)$"
        )] | None = None # type: ignore
    
    @field_validator('service_id')
    def check_service_id(cls, v):
        if v not in ["dstv","gotv","startimes","abuja-electric","eko-electric","ibadan-electric","ikeja-electric","jos-electric","kaduna-electric","kano-electric","portharcout-electric"]:
            raise ValueError("Service id is not recognised")
        return v
    
    @field_validator('variation_id')
    def check_variation_id(cls, v):
        if v and v not in ["prepaid", "postpaid"]:
            raise ValueError("Variation id is not recognised")
        return v
    
    @field_validator('customer_id')
    def check_customer_id(cls, v):
        if len(v) < 10 or len(v) > 11:
            raise ValueError("Customer id is not complete")
        return v


class VerifyResponse(BaseModel):
    code: Optional[str]
    message: Optional[str]
    customer_id: Optional[str]
    customer_address: Optional[str]
    customer_arrears: Optional[str]
    decoder_status: Optional[str]
    decoder_due_date: Optional[str]
    decoder_balance: Optional[str]
    
    @classmethod
    def get_info(cls, data: dict):
        if data.get("code") == "success":
            return cls(
                code=data.get('code'),
                message=data.get('message'),
                customer_id=data['data'].get('customer_id'),
                customer_address=data['data'].get('customer_address'),
                customer_arrears=data['data'].get('customer_arrears'),
                decoder_status=data['data'].get('decoder_status'),
                decoder_due_date=data['data'].get('decoder_due_date'),
                decoder_balance=data['data'].get('decoder_balance')
            )
        elif data.get("code") == "failure":
            return cls(
                code=data.get('code'),
                message=data.get('message')
            )
        else:
            raise ValueError("Invalid or unknown data passed ")
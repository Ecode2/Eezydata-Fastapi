from pydantic import BaseModel, constr, field_validator
from typing import Optional


class CableModel(BaseModel):
    phone: constr(strip_whitespace=True, min_length=11, max_length=11) # type: ignore
    service_id: constr(
        strip_whitespace=True, 
        pattern=r"^(dstv|gotv|startimes)$"
        ) # type: ignore 
    variation_id: constr(
        strip_whitespace=True, 
        pattern=r"^(dstv-padi|dstv-yanga|dstv-confam|dstv6|dstv79|dstv7|dstv3|dstv10|dstv9|confam-extra|yanga-extra|padi-extra|com-asia|dstv30|com-frenchtouch|dstv33|dstv40|com-frenchtouch-extra|com-asia-extra|dstv43|complus-frenchtouch|dstv45|complus-french-extraview|dstv47|dstv48|dstv61|dstv62|hdpvr-access-service|frenchplus-addon|asia-addon|frenchtouch-addon|extraview-access|french11|gotv-smallie|gotv-jinja|gotv-jolli|gotv-max|gotv-supa|nova|basic|smart|classic|super)$"
        ) # type: ignore
    smartcard_number: constr(strip_whitespace=True, min_length=10, max_length=10) # type: ignore
    
    @field_validator('phone')
    def check_phone(cls, v):
        if len(v) != 11 :
            raise ValueError("Phone number is not complete")
        return v
    
    @field_validator('smartcard_number')
    def check_smartcard_number(cls, v):
        if len(v) != 10 :
            raise ValueError("Smartcard_number number is not complete")
        return v
    
    @field_validator('service_id')
    def check_service_id(cls, v):
        if v not in ["dstv","gotv","startimes"]:
            raise ValueError("Service id is not recognised")
        return v
    
    @field_validator('variation_id')
    def check_variation_id(cls, v):
        if v not in ["dstv-padi","dstv-yanga","dstv-confam","dstv6","dstv79","dstv7","dstv3","dstv10","dstv9","confam-extra","yanga-extra","padi-extra","com-asia","dstv30","com-frenchtouch","dstv33","dstv40","com-frenchtouch-extra","com-asia-extra","dstv43","complus-frenchtouch","dstv45","complus-french-extraview","dstv47","dstv48","dstv61","dstv62","hdpvr-access-service","frenchplus-addon","asia-addon","frenchtouch-addon","extraview-access","french11","gotv-smallie","gotv-jinja","gotv-jolli","gotv-max","gotv-supa","nova","basic","smart","classic","super"]:
            raise ValueError("Variation id is not recognised")
        return v


class CableResponse(BaseModel):
    code: Optional[str]
    message: Optional[str]
    cable_tv: Optional[str]
    smartcard_number: Optional[str]
    subscription_plan: Optional[str]
    service_fee: Optional[str]
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
                cable_tv=data['data'].get('cable_tv'),
                smartcard_number=data['data'].get('smartcard_number'),
                subscription_plan=data['data'].get('subscription_plan'),
                service_fee=data['data'].get('service_fee'),
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
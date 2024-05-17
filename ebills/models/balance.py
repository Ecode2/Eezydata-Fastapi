from pydantic import BaseModel
from typing import Optional, List


class BalanceResponse(BaseModel):
    code: Optional[str]
    message: Optional[str]
    balance: Optional[str]
    currency: Optional[str]
    
    @classmethod
    def get_info(cls, data: dict):
        if data.get("code") == "success":
            return cls(
                code=data.get('code'),
                message=data.get('message'),
                balance=data['data'].get('balance'),
                currency=data['data'].get('currency')
            )
        elif data.get("code") == "failure":
            return cls(
                code=data.get('code'),
                message=data.get('message')
            )
        else:
            raise ValueError("Invalid or unknown data passed ")
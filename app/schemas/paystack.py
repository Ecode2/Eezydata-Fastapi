"""Schemas for paystack wallet."""
from typing import Optional
from pydantic import BaseModel, Field

class PaystackPublic(BaseModel):
    """Response for wallet information endpoint."""
    user_id: int = Field(None, example=1173)
    user_code: str = Field(None, example="CUS_xnxdt6s1zg1f4nx")
    authUser_id: str = Field(None, example="16fd2706-8baf-433b-82eb-8c7fada847da")
    account_name: str = Field(None, example="KAROKART / RHODA CHURCH")
    bvn: str = Field(None, example="09053334749")
    bank: str = Field(None, example="Wema Bank")
    account_id: int = Field(None, example=253)
    account_number: str = Field(None, example="9930000737")
    is_active: Optional[bool] = Field(True, example="true")


class PaystackCreate(BaseModel):
    id: int
    authUser_id: str
    customer_code: str
    integration: int
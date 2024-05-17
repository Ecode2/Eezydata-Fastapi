from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class PriceModel(BaseModel):
    bill_type: str = Field(..., example="electric")
    brand: str = Field(..., example="IBEDC")
    code: str = Field(None, example="prepaid")


class PricesPublic(BaseModel):
    """Response Model for price information endpoint."""
    bill_type: str = Field(..., example="electric")
    brand: str = Field(..., example="IBEDC")
    name: str = Field(..., example="Price per KiloWatt")
    code: str = Field(..., example="prepaid")
    price: str = Field(None, example="500")
 

class PriceUpdate(BaseModel):
    """Model for price update endpoint."""
    bill_type: str = Field(None, example="electric")
    brand: str = Field(None, example="IBEDC")
    name: str = Field(None, example="Price per KiloWatt")
    code: str = Field(None, example="prepaid")
    price: str = Field(None, example="500")


class BillsModel(BaseModel):
    """Model for price update endpoint."""
    bill_type: str = Field(None, example="electric")
    brand: str = Field(None, example="IBEDC")
    name: str = Field(None, example="Price per KiloWatt")
    code: str = Field(None, example="prepaid")
    price: str = Field(None, example="500")
    phone: str = Field(None, example="09060636536")
    variation: str = Field(None, example="500")
    meter: str = Field(None, example="500")
    smartcard: str = Field(None, example="500")
    amount:int = Field(None, example=500)
    user_id: str = Field(None, example="500")
    wallet_id: str = Field(None, example="500")


class RecordsPublic(BaseModel):
    transaction_id:str  = Field(None, example="electric")
    authUser_id:str  = Field(None, example="electric")
    order_id:str  = Field(None, example="electric")
    message:str  = Field(None, example="electric")
    status:str  = Field(None, example="electric")
    bill_type:str  = Field(None, example="electric")
    brand:str  = Field(None, example="electric")
    name:str  = Field(None, example="electric")
    price:str  = Field(None, example="electric")
    created_at:str  = Field(None, example="electric")

#TODO: create a model for cable, electric, data and airtime 
# => public when the bill is bought
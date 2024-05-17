"""The main APIRouter is defined to include all the sub routers from each
module inside the API folder"""
from fastapi import APIRouter
from .base import base_router
from .routes.auth.auth import auth_router
from .routes.bills.bills import bill_router
from .routes.account.paystack import paystack_router

api_router = APIRouter()
api_router.include_router(base_router, tags=["base"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(bill_router, prefix="/bills", tags=["bills"])
api_router.include_router(paystack_router, prefix="/paystack", tags=["paystack"])
import datetime, uuid, logging
from typing import Union, Any
from fastapi import HTTPException, status
from passlib.context import CryptContext  # type: ignore
from sqlalchemy import Column, String, Boolean, DateTime  # type: ignore
from sqlalchemy.orm import Session, relationship, backref
from app.configs import get_settings
from app.db.models.ebills import Prices
from app.schemas.bills import PricesPublic  # type: ignore
from ..base import Base
from ..session import session_scope
from ...schemas.auth import AuthUserPublic

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


def get_plan(raw: bool = False, **kwargs)-> PricesPublic:

    if not kwargs.get('bill_type') or not kwargs.get('brand'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Information inaccurate")

    with session_scope() as session:

        prices= Prices.get_prices(
            db_session=session,
            bill_type=kwargs.get('bill_type'),
            brand=kwargs.get('brand'),
            code=kwargs.get('code'),
            populate= True if raw else False
        )

        msg = "{} [{}] prices.".format(str("Got").capitalize, kwargs.get('brand'))
        logger.info(msg)

        return prices
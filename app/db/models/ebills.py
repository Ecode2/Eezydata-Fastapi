"""User table for paystack information."""
import datetime, uuid
from typing import List, Union, Any
from passlib.context import CryptContext  # type: ignore
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime  # type: ignore
from sqlalchemy.orm import Session
from app.schemas.bills import PricesPublic, RecordsPublic
from app.schemas.paystack import PaystackPublic  # type: ignore
from ..base import Base
from ..session import session_scope
from ...schemas.auth import AuthUserPublic



class Prices(Base):
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()), unique=True)
    bill_type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    price = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        default=datetime.datetime.utcnow())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=datetime.datetime.utcnow())
    #TODO: add an actual price row to show the actual ebills price

    @classmethod
    def add_price(cls, bill_type: str, brand: str,
                      name: str, code: str,
                      price: str):
        """Create a new bill Price.

        Args:
            bill_type (str): type of bill like [data, airtime, cable, electric]
            brand (str): chosen bill brand [mtn, glo, airtel, 9moile]
            name (str): Bills name 
            code (str): unique code identifier
            price (dict): the cost of the bill

        Returns:
            Price: newly created wallet instance.
        """
        return cls(bill_type=bill_type, brand=brand,
                      name=name, code=code,
                      price=price)  # type: ignore

    @classmethod
    def get_prices(cls,
                  db_session: Session,
                  bill_type: str,
                  brand: str,
                  code: str = None,
                  populate: bool = False) -> Any | List[Any]:
        """Get the corresponding wallet with given user id in DB.

        Args:
            db_session (:obj:`sqlalchemy.orm.Session`): DB session for getting
              the user corresponding given user id.
            bill_type (str): type of bill like [data, airtime, cable, electric]
            brand (str): chosen bill brand [mtn, glo, airtel, 9moile]
            code (str): unique code identifier
            populate (bool): if True, returns a public user profile (without unecessary info).

        Returns:
            Union[None, List[PricesPublic], PricesPublic]: list wallet if not code or wallet or None.

        """

        if code:
            prices = db_session.query(cls).filter_by(bill_type = bill_type, brand=brand, code=code).first()
        else:
            prices = db_session.query(cls).filter_by(bill_type = bill_type, brand=brand).all()
        
        if not prices:
            return None

        if not populate:
            return prices
        
        if code:
            return PricesPublic(**prices._asdict()) if prices else prices
        
        return [PricesPublic(**price._asdict()) for price in prices] if prices else prices

    def __repr__(self):
        return f'<Price {self.brand}>'

class History(Base):
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()), unique=True)
    transaction_id = Column(String, ForeignKey("transactions.id"), default=None)
    authUser_id = Column(String, ForeignKey("authuser.id"))
    wallet_id = Column(String, ForeignKey("wallet.id"))
    order_id = Column(String, unique=True, nullable=False)
    message = Column(String, nullable=False)
    status = Column(String, nullable=False)
    bill_type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    price = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        default=datetime.datetime.utcnow())

    @classmethod
    def get_record(cls,
                  db_session: Session,
                  authUser_id:str,
                  order_id:str,
                  transaction_id:str = None,
                  populate: bool = False) -> Any | List[Any]:
        """Get the corresponding history record of the user id.

        Args:
            db_session (:obj:`sqlalchemy.orm.Session`): DB session for getting
              the user corresponding given user id.
            authUser (str): current user id
            order_id (str): bill order id received
            transaction_id (Optional[str]): unique id of payment transaction
                required only for specific records
            populate (bool): if True, returns a public history record.

        Returns:
            Union[None, List[RecordsPublic], RecordsPublic]: list of records if transaction id is none.

        """
        if transaction_id:
            records = db_session.query(cls).filter_by(authUser_id = authUser_id, order_id=order_id, transaction_id=transaction_id).first()
        else:
            records = db_session.query(cls).filter_by(authUser_id = authUser_id, order_id=order_id).all()
        
        if not records:
            return None

        if not populate:
            return records
        
        if transaction_id:
            return RecordsPublic(**records._asdict()) if records else records
        
        return [RecordsPublic(**record._asdict()) for record in records] if records else records


    @classmethod
    def create_new_record(cls, transaction_id: str, authUser_id: str,
                      wallet_id: str, order_id: str,
                      status: str, **kwargs):
        """Create a new Bill Payment record.

        Args:
            transaction_id (str): od of the wallet transaction.
            authUser_id (str): uuid of the current user.
            wallet_id (str): wallet id of paystack Wallet table.
            orde_id (str): orde_id of the bill transaction.
            status (str): status code of the bill transaction [success, failure]
            kwargs (dict): other user information.

        Returns:
            History: newly created bill History instance.
        """
        return cls(transaction_id=transaction_id,
                   authUser_id=authUser_id,
                   wallet_id=wallet_id,
                   order_id=order_id,
                   status=status,
                   **kwargs)

    def __repr__(self):
        return f'<History {self.id}>'
    
    
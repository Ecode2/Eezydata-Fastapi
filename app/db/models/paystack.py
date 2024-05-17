"""Wallet table for paystack information."""
import datetime, uuid
from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime  # type: ignore
from sqlalchemy.orm import Session, relationship

from app.schemas.paystack import PaystackPublic  # type: ignore
from ..base import Base



class Wallet(Base):
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()), unique=True)
    authUser_id = Column(String, ForeignKey("authuser.id"))
    user_id = Column(Integer, unique=True, nullable=False)
    user_code = Column(String, unique=True, nullable=False)
    account_number = Column(String, unique=True, default=None, nullable=True)
    account_id = Column(Integer, unique=True, default=None, nullable=True)
    bank = Column(String, unique=True, default=None, nullable=True)
    account_name = Column(String, unique=True, default=None, nullable=True)
    authorization = Column(String, unique=True, default=None, nullable=True)
    signature = Column(String, unique=True, default=None, nullable=True)
    bvn = Column(String, unique=True, default=None, nullable=True)
    integration = Column(Integer, unique=True, nullable=False)
    identified = Column(Boolean, default=False)
    total_transactions = Column(Integer, default=0)

    history = relationship("History", backref="wallet", lazy=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        default=datetime.datetime.utcnow())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=datetime.datetime.utcnow())

    @classmethod
    def get_wallet(cls,
                 db_session: Session,
                 authUser_id: str,
                 populate: bool = False) -> PaystackPublic | Any:
        """Get the corresponding wallet with given user id in DB.

        Args:
            db_session (:obj:`sqlalchemy.orm.Session`): DB session for getting
              the user corresponding given user id.
            authUser_id (str): user id for searching wallet.
            populate (bool): if True, returns a public user profile (without unecessary info).

        Returns:
            Union[None, PaystackPublic]: found wallet or None.
        """
        wallet = db_session.query(cls).filter(cls.authUser_id == authUser_id).scalar()
        if not populate:
            return wallet
        return PaystackPublic(**wallet._asdict()) if wallet else wallet
    

    @classmethod
    def create_wallet(cls, 
                      user_id: int, authUser_id: str,
                      user_code: str, integration: int,
                       **kwargs):
        """Create a new paystack customer.

        Args:
            user_id (int): customer id of paystack.
            authUser_id (str): uuid of the current user.
            user_code (str): customer code of paystack.
            integration (int): integration number of the paystack customer.
            kwargs (dict): other user information.

        Returns:
            Wallet: newly created wallet instance.
        """

        return cls(user_id=user_id, 
                   authUser_id=authUser_id,
                   user_code=user_code,
                   integration=integration,
                   **kwargs)  # type: ignore
    
    def __repr__(self):
        return f'<Wallet {self.user_code}>'

class Transactions(Base):
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()), unique=True)
    history = relationship("History", backref="transactions", lazy=True)
    
#TODO: create a transaction table that stores all transactions made my a 
# wallet with wallet id foreign key
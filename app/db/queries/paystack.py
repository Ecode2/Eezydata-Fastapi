"""Define functions quering Wallet table."""
# mypy: ignore-errors
import logging
from ..models import AuthUser, Wallet
from ..session import session_scope
from ...schemas.auth import AuthUserPublic
from ...configs import get_settings

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


async def get_wallet_info(username: str):
    """Get current user wallet information

    Args:
        username: User name of current user

    Returns:
        
    """ 
    with session_scope() as session:

        user_info = session.query(AuthUser).filter( username == username ).scalar()
        
        if not user_info and  user_info.is_active == False:

            msg = f"User doesn't exists or is not active."
            logger.error(msg)
            return False
        
        wallet_info = Wallet.get_wallet(session, user_info.id, )

        return wallet_info

"""Define functions quering AuthUser table."""
# mypy: ignore-errors
import logging
from ..models import AuthUser
from ..session import session_scope
from ...schemas.auth import AuthUserPublic
from ...configs import get_settings

settings = get_settings()
logger = logging.getLogger(settings.PROJECT_SLUG)


def validate_info(info: str, info_type, is_superuser: bool = False):
    """Check if user info is already in use.

    Args:
        info (str): User info.
        info_type (str): type of info to be confirmed.
        is_superuser (bool, optional): the user will be a superuser.

    Returns:
        bool: returns true or false depending on the validation.
    """ 
    with session_scope() as session:
        user_exists = session.query(AuthUser).filter( info_type == info ).scalar()
        
        if is_superuser and user_exists and user_exists.is_superuser == False:
            msg = f"{str(info_type).capitalize} [{info}] is not a superuser."
            logger.error(msg)
            return False

        elif user_exists:
            msg = f"{str(info_type).capitalize} [{info}] is used already."
            logger.error(msg)
            return False

        msg = f"{str(info_type).capitalize} [{info}] is available."
        logger.info(msg)
        return True
    
#TODO: create a function that updates user balance from authUser table
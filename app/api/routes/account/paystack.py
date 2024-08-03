"""Bills Payment related endpoints."""
import logging
from fastapi import Depends, HTTPException, Query, status, APIRouter
from app.db.queries.paystack import get_wallet_info
from app.schemas.auth import AuthUserPublic
from ebills.models.verify import VerifyModel, VerifyResponse
from ebills import Verify
from ....utils.security import (get_current_active_user, http_auth)
from ....configs import get_settings


settings = get_settings()
paystack_router = APIRouter()
logger = logging.getLogger(settings.PROJECT_SLUG)


@paystack_router.get("/info",
                  dependencies=[Depends(http_auth)])
async def Account_info(username: str = Query(None), current_user: AuthUserPublic = Depends(get_current_active_user)):
    """Get paystack Account Information

    \f

    Args:
        current_user (:obj:`..schemas.auth.User`): the corresponding user of the
          pass token.

    Returns:
    """

    if username != current_user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User is unauthorised to access this page.")

    wallet_info = await  get_wallet_info(username=username)

    if not wallet_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldnt get wallet info.")
    
    return wallet_info

@paystack_router.get("/webhook")
async def receive_webhook():
    pass


#TODO: create an endpoint to receive webhooks made by transfers
# => and store the info in the appropriate table with the customer_code
# => as the search item 
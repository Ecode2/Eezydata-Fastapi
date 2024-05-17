"""Bills Payment related endpoints."""
import logging
from fastapi import Depends, HTTPException, status, APIRouter
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
async def Account_info(current_user: AuthUserPublic = Depends(get_current_active_user)):
    """Get paystack Account Information

    \f

    Args:
        current_user (:obj:`..schemas.auth.User`): the corresponding user of the
          pass token.

    Returns:
    """

    pass
    #TODO: create a function that gets user balance from authUser table

@paystack_router.get("/webhook")
async def receive_webhook():
    pass


#TODO: create an endpoint to receive webhooks made by transfers
# => and store the info in the appropriate table with the customer_code
# => as the search item 
"""OAuth2 authentication and user related endpoints."""
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, Query, status, APIRouter, Body, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import session_scope
from app.services import paystack_create_user
from ....db.models import AuthUser
from ....db.queries import validate_info
from jose import JWTError, jwt  # type: ignore
from ....schemas.auth import (
    AuthTokenPublic, AuthUserUpdate, Token, AuthUserPublic, AuthUserCreationForm, LoginForm
)
from ....utils.security import (
    create_access_token, get_current_active_user, http_auth
)
from ....utils.storage import store_user, update_user
from ....configs import get_settings


settings = get_settings()
auth_router = APIRouter()


@auth_router.post("/token", response_model=AuthTokenPublic)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> AuthTokenPublic: #LoginForm = Body()) -> Token:
    """Login with credentials to get access token.

    \f

    Args:
        form_data (:obj:`LoginForm`): contains username and password.

    Returns:
        :obj:`Token`: create access token.

    Raises:
        :obj:`HTTPException`: if not authenticated user, or user is inactive.
    """
    
    user = AuthUser.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    elif user.is_superuser:  # type: ignore
        expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN
    else:
        expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(days=expire_minutes)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires  # type: ignore
    )
    token = Token(access_token=access_token, token_type="Bearer") 
    

    return AuthTokenPublic(**token.model_dump(), **user.model_dump())  # nosec


@auth_router.post("/user/new",
                  response_model=AuthUserPublic,)
async def create_user(background_task: BackgroundTasks, form_data: AuthUserCreationForm = Body(None)) -> AuthUserPublic:
    """Create a new user.
    \f

    Args:
        form_data (UserCreationForm): form data containing new user's
          credentials and information.

    Returns:
        AuthUserPublic: a brief of newly created user.
    """
    
    if not validate_info(info=form_data.username, info_type=AuthUser.username) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username is in use.")
    if not validate_info(info=form_data.email, info_type=AuthUser.email) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email is already taken.")
    if not validate_info(info=form_data.phone, info_type=AuthUser.phone) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Phone number is already taken.")

    try:
        user = store_user(**form_data.model_dump(), raw=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to store in DB. error {e}")
    if not AuthUserPublic(**user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists.")
    
    # Task to create all paystack information
    background_task.add_task(paystack_create_user, user)

    # TODO: Background function to authenticate users email and phone

    return AuthUserPublic(**user)


@auth_router.get("/user/info",
                 response_model=AuthUserPublic,
                 dependencies=[Depends(http_auth)])
async def get_user_info(
        current_user: AuthUserPublic = Depends(get_current_active_user)) \
        -> AuthUserPublic:
    """Use the access token to get the current user's account information.

    \f

    Args:
        current_user (:obj:`..schemas.auth.User`): the corresponding user of the
          pass token.

    Returns:
        :obj:`..schemas.auth.User`: the corresponding user of the
          pass token.
    """
    return current_user


@auth_router.put("/user/update",
                 response_model=AuthUserPublic,
                 dependencies=[Depends(http_auth)])
async def update_user_info(username: str = Query(None), password: str = Query(""), form_data: AuthUserUpdate = Body(None),
        current_user: AuthUserPublic = Depends(get_current_active_user)) \
        -> AuthUserPublic:
    """Use the username to update the current user's account information.

    \f

    Args:
        username (str): the username of the user
        password (str, optional): the password of the user
        current_user (:obj:`..schemas.auth.User`): the corresponding user of the
          pass token.

    Returns:
        :obj:`..schemas.auth.User`: the corresponding user of the
          pass token.
    """
    if not validate_info(info=form_data.username, info_type=AuthUser.username) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with username {username} doesn't exist.")
    
    try:
        user_update = update_user(user=username, secret=password, **form_data.dict())

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to update DB info. error {e}")
    if not user_update:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Username or password is incorrect.")

    return current_user


@auth_router.post("/user/verify",
                 response_model=bool)
async def verify_user_info(form_data: AuthUserUpdate = Body(None)) -> bool:
    """Verify if a user exists using email or username.

    \f

    Args:
        form_data (AuthUserUpdate): form data containing either username or email or both

    Returns:
        bool: returns a  False if user doesn't exists
        and raises a 400 HTTP error if user exists
    """
    
    if form_data.username and not validate_info(info=form_data.username, info_type=AuthUser.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username is in use.")
    
    if form_data.email and not validate_info(info=form_data.email, info_type=AuthUser.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email is in use.")
    
    return False

@auth_router.post("/user/confirm",
                 response_model=bool)
async def confirm_token(token: str = Query(None)) -> bool:
    """Confirm a users token
    \f
    Args:
        token Query(str): json web token in the query parameters

    Returns:
        bool: returns a  False if token is invalid
              and True if token is valid
    """
    try:
        payload = jwt.decode(token,
                             settings.SECRET_KEY,
                             algorithms=[settings.JWT_ENCODE_ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            return False
    except JWTError:
        return False
    
    with session_scope() as session:
        user = AuthUser.get_user(session, username, populate=True)

    if not user or not user.is_active:
        return False
    
    return True
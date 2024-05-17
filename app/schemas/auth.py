"""Schemas for authentication."""
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Form, Body


class Token(BaseModel):
    """Response for login to access token endpoint."""
    access_token: str = Field(...,
                              example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                      "eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjI0NT"
                                      "YzMDAzfQ.SXuWTMZ0XvxCJN5uGt6ktQL59V5HrP"
                                      "jPZYu7tr6n9GY")
    token_type: str = Field("Bearer",
                            description="Type of the token.",
                            example="Bearer")


class AuthUserPublic(BaseModel):
    """Response for read_users_me endpoint."""
    username: str = Field(..., example="johndoe")
    email: str = Field(..., example="john.doe@example.com")
    firstname: str = Field(..., example="John")
    lastname: str = Field(..., example="Doe")
    balance: Optional[float] = Field(None, example=0.0)
    wallet_type: Optional[str] = Field(None, example="paystack")
    phone: str = Field(..., example="09053334749")
    is_active: Optional[bool] = Field(True, example="true")
    is_superuser: Optional[bool] = Field(False, example="false")

class AuthTokenPublic(BaseModel):
    """Response for login user endpoint."""
    
    username: str = Field(..., example="johndoe")
    email: str = Field(..., example="john.doe@example.com")
    firstname: str = Field(..., example="John")
    lastname: str = Field(..., example="Doe")
    balance: Optional[float] = Field(None, example=0.0)
    wallet_type: Optional[str] = Field(None, example="paystack")
    phone: str = Field(..., example="09053334749")
    is_active: Optional[bool] = Field(True, example="true")
    is_superuser: Optional[bool] = Field(False, example="false")
    access_token: str = Field(...,
                              example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                      "eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjI0NT"
                                      "YzMDAzfQ.SXuWTMZ0XvxCJN5uGt6ktQL59V5HrP"
                                      "jPZYu7tr6n9GY")
    token_type: str = Field("Bearer",
                            description="Type of the token.",
                            example="Bearer")

class AuthUserUpdate(BaseModel):
    """Request for update_users_me endpoint."""
    username: Optional[str] = Field(None, example="johndoe")
    email: Optional[str] = Field(None, example="john.doe@example.com")
    firstname: Optional[str] = Field(None, example="John")
    lastname: Optional[str] = Field(None, example="Doe")
    phone: Optional[str] = Field(None, example="09053334749")
    password: Optional[str] = Field(None, example="secret")
    picture: Optional[str] = Field(None, example="image/profile.jpg")
    is_active: Optional[bool] = Field(True, example="true")
    is_superuser: Optional[bool] = Field(False, example="false")


class LoginForm(BaseModel):
    """Request form for login to getting tokens."""
    username: str = Field(..., description="Username", example="johndoe")
    password: str = Field(..., description="Password in plaintext",
                          example="secret")

    def __init__(self,
                 username: str = Body(...),
                 password: str = Body(...)):
        super().__init__(username=username, password=password)


class AuthUserCreationForm(BaseModel):
    """Request form for creating a new user."""
    username: str = Field(..., description="Username", example="johndoe")
    firstname: str = Field(..., description="First name", example="John")
    lastname: str = Field(..., description="Last name", example="Doe")
    phone: str = Field(..., description="Phone number", example="09053334749")
    password: str = Field(..., description="Password in plaintext",
                          example="secret")
    email: str = Field( description="Email address",
                       example="john.doe@example.com")
    

    def __init__(self,
                 username: str = Body(...),
                 firstname: str = Body(...),
                 lastname: str = Body(...),
                 phone: str = Body(...),
                 password: str = Body(...),
                 email: str = Body(...)):
        super().__init__(username=username, firstname=firstname,
                         lastname=lastname, phone=phone,
                         password=password, email=email)

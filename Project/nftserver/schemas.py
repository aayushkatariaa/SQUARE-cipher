from pydantic import BaseModel

from pydantic import BaseModel
from typing import Optional
class User(BaseModel):
    username: str
    email: str
    password: str
    wallet_balance: Optional[float] = 100.0
class Login(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None
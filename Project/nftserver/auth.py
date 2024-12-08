from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "your_jwt_secret_key"

@AuthJWT.load_config
def get_config():
    return Settings()

def get_current_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        return Authorize.get_jwt_subject()
    except AuthJWTException:
        raise HTTPException(status_code=401, detail="Invalid token")

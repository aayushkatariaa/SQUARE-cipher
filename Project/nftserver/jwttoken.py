from datetime import datetime, timedelta
from jose import JWTError, jwt
from services import get_user_by_email

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(subject: str):
    to_encode = {"sub": subject}  # Add subject as a claim
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        # Fetch user details using the username
        user = get_user_by_email(email)
        if user is None:
            raise credentials_exception
        
        # Create and return the full user data (with all relevant fields)
    except JWTError:
        raise credentials_exception

    return user
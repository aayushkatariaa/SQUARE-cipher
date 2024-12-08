from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Request,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwttoken import create_access_token
from oauth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from services import get_user_by_email, create_user, verify_password,buy_artwork, create_artwork, get_all_artworks,get_artwork_by_id,encrypt_metadata,get_owned_artworks

app = FastAPI()
origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    username: str
    email: str
    password: str
    wallet_balance: Optional[float] = 100.0
    
class Login(BaseModel):
	email: str
	password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None
class ArtworkUpload(BaseModel):
    title: str
    description: str
    price: float
    image_url: str
class Artwork(BaseModel):
    id: str = None
    title: str
    description: str
    price: float
    image_url: str
    owner_id: str = None  # Links to User who owns it
    encrypted_metadata: str


@app.get("/")
def read_root(current_user:User = Depends(get_current_user)):
	return {"data":"Hello OWrld"}

@app.post('/register')
def register(user:User):
	existing_user = get_user_by_email(user.email)
	if existing_user:
		raise HTTPException(status_code=400, detail="User already exists")
	create_user(user.email, user.password,user.username)
	return {"message": "User created successfully"}

@app.post("/login")
def login(user:Login):
    print(user)
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token}

@app.get("/wallet_balance")
def wallet_balance(current_user: User = Depends(get_current_user)):
    print(current_user)
    return {"wallet_balance": current_user['wallet_balance']}

@app.post("/buy_nft/{artwork_id}")
def buy_nft(artwork_id: str, current_user: User = Depends(get_current_user)):
    return  buy_artwork(artwork_id,current_user)

# Upload artwork (restricted to logged-in users)
@app.post("/upload_artwork/")
def upload_artwork(data: ArtworkUpload, current_user: User = Depends(get_current_user)):
    print(current_user)
    encrypted_metadata = encrypt_metadata(
        f"{data.title}:{data.description}:{data.price}", current_user["username"]
    )
    artwork = {
        "title": data.title,
        "description": data.description,
        "price": data.price,
        "image_url": data.image_url,
        "owner_id": current_user,
        "encrypted_metadata": encrypted_metadata,
    }
    create_artwork(artwork)
    return {"message": "Artwork uploaded successfully"}

# # Get all artworks
@app.get("/artworks")
def get_artworks():
    return get_all_artworks()

 # Route to get all artworks
@app.get("/owned/")
def owned(current_user: User = Depends(get_current_user)):
    return get_owned_artworks(current_user)

# # Route to decrypt artwork metadata
# @app.get("/decrypt_metadata/{artwork_id}")
# def decrypt_artwork_metadata(artwork_id: str, secret_key: str):
#     artwork = get_artwork_by_id(artwork_id)
#     decrypted_metadata = decrypt_metadata(artwork["encrypted_metadata"], secret_key)
#     return {"decrypted_metadata": decrypted_metadata}
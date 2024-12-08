import bcrypt
from pymongo import MongoClient
from fastapi import HTTPException
from cryptography.fernet import Fernet
from square import encrypt, decrypt
import os
from dotenv import load_dotenv
from bson import ObjectId
# import cloudinary.uploader
# import cloudinary.api
from schemas import User
from fastapi.responses import JSONResponse
load_dotenv()

# MongoDB connection
mongodb_uri = 'mongodb+srv://sudeep160403:1234@cluster0.ktcec.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(mongodb_uri)
db = client["nft_marketplace"]
users_collection = db["users"]
artworks_collection = db["artworks"]

# # Password hashing
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def ensure_16_bytes(data: bytes) -> bytes:
    """Ensure the byte data is exactly 16 bytes long by padding or trimming."""
    if len(data) < 16:
        # Pad with zero bytes if data is too short
        return data.ljust(16, b'\x00')
    elif len(data) > 16:
        # Trim if data is too long
        return data[:16]
    return data

def encrypt_metadata(metadata: str, secret_key: str) -> str:
    # Convert metadata and secret_key to bytes
    metadata_bytes = metadata.encode('utf-8')  # Encoding string to bytes
    secret_key_bytes = secret_key.encode('utf-8')  # Encoding secret_key to bytes
    
    # Ensure both the metadata and key are 16 bytes long
    metadata_bytes = ensure_16_bytes(metadata_bytes)
    secret_key_bytes = ensure_16_bytes(secret_key_bytes)
    
    # Encrypt the metadata using the provided secret key
    encrypted_metadata = encrypt(metadata_bytes, secret_key_bytes)
    
    return encrypted_metadata.hex() 
    # cipher = Fernet(secret_key.encode())
    # return cipher.encrypt(metadata.encode()).decode()
def decrypt_metadata(encrypted_metadata: str, secret_key: str) -> str:
    # Convert encrypted_metadata and secret_key to bytes
    # encrypted_metadata_bytes = bytes.fromhex(encrypted_metadata)
    secret_key_bytes = secret_key.encode('utf-8')  # Encoding secret_key to bytes
    
    # Ensure both the encrypted_metadata and key are 16 bytes long
    encrypted_metadata_bytes = ensure_16_bytes(encrypted_metadata_bytes)
    secret_key_bytes = ensure_16_bytes(secret_key_bytes)
    
    # Decrypt the encrypted metadata using the provided secret key
    decrypted_metadata = decrypt(encrypted_metadata_bytes, secret_key_bytes)

# # User operations
def create_user(email: str, password: str, username:str):
    hashed_password = hash_password(password)
    user = {"email": email, "password": hashed_password, "wallet_balance": 100.0, "username":username}
    users_collection.insert_one(user)

def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})
def get_user_by_username(username: str):
    return users_collection.find_one({"username": username})


def buy_artwork(artwork_id: str, user: User):
    # Fetch the artwork from the database
    artworks = artworks_collection.find_one({"_id": ObjectId(artwork_id)})
    if not artworks:
        raise HTTPException(status_code=404, detail="Artwork not found")
    
    # Check if the user has sufficient wallet balance
    if user["wallet_balance"] < artworks["price"]:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Deduct the wallet balance
    users_collection.update_one(
        {"email": user["email"]},
        {"$inc": {"wallet_balance": -artworks["price"]}}
    )
    print(artworks)
    encrypted_metadata = encrypt_metadata(
        f"{artworks["title"]}:{artworks["description"]}:{artworks["price"]}", user["username"]
    )
    # Update the artwork with the new metadata and assign ownership
    artworks_collection.update_one(
        {"_id": ObjectId(artwork_id)},
        {
            "$set": {
                "owner_id": user,
                "encrypted_metadata": encrypted_metadata
            }
        }
    )
    
    return {
        "message": "Artwork purchased successfully",
        "new_encrypted_metadata": encrypted_metadata
    }


# # Artwork operations
def create_artwork(data: dict):
    artworks_collection.insert_one(data)

def get_all_artworks():
    artworks = artworks_collection.find()
    result = []
    for artwork in artworks:
        owner = artwork.get("owner_id")
        # Convert owner details if necessary
        if isinstance(owner, ObjectId):
            owner = str(owner)
        elif isinstance(owner, dict):
            # Convert ObjectId fields within the owner dictionary to strings
            owner = {key: str(value) if isinstance(value, ObjectId) else value for key, value in owner.items()}
        
        result.append({
            "id": str(artwork["_id"]),
            "title": artwork["title"],
            "image_url": artwork["image_url"],
            "price": artwork["price"],
            "description": artwork["description"],
            "metadata": artwork["encrypted_metadata"],
            "owner": owner
        })
        print(result)
    return result    # return list(artworks_collection.find())

# # Helper to fetch artwork
def get_artwork_by_id(artwork_id: str):
    artwork = artworks_collection.find_one({"_id": ObjectId(artwork_id)})
    if not artwork:
        return JSONResponse(status_code=404, content={"message": "Artwork not found"})
    
    return artwork

def get_owned_artworks(user: User):
    print(user)
    print(list(artworks_collection.find({"owner_id": user})))
    return list(artworks_collection.find({"owner_id": user}))

# # Cloudinary configuration
# cloudinary.config(
#     cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
#     api_key=os.getenv('CLOUDINARY_API_KEY'),
#     api_secret=os.getenv('CLOUDINARY_API_SECRET')
# )

# def upload_image_to_cloudinary(image_path: str):
#     """Uploads the image to Cloudinary and returns the URL."""
#     response = cloudinary.uploader.upload(image_path)
#     return response['secure_url']

# def encrypt_metadata(metadata: str, key: str) -> str:
#     """Encrypts the metadata using Square Cipher and AES."""
#     key = hashlib.sha256(key.encode()).digest()
#     cipher = AES.new(key, AES.MODE_EAX)
#     ciphertext, tag = cipher.encrypt_and_digest(metadata.encode())
#     return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

# def decrypt_metadata(encrypted_metadata: str, key: str) -> str:
#     """Decrypts the metadata."""
#     encrypted_data = base64.b64decode(encrypted_metadata)
#     nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
#     key = hashlib.sha256(key.encode()).digest()
#     cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
#     return cipher.decrypt_and_verify(ciphertext, tag).decode()



from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from models.models import Partner
from internal.keys import decrypt_secret_key
from pymongo.database import Database
from database import get_db

# NOTE: We need to store this in a .env file
ALGORITHM = "HS256"
SECRET_KEY = "123456789"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_partner(token: str = Security(oauth2_scheme), db: Database = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        shopify_store_id = payload.get("sub")
        if shopify_store_id is None:
            raise credentials_exception
        company_info = await get_partner_info(db, shopify_store_id)
        if company_info is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return company_info


async def get_partner_info(db, shopify_store_id: str) -> Partner | None:
    company_data = db.companies.find_one( {"shopify_store_id": shopify_store_id})
    if company_data:
        encrypted_secret_key = company_data.get("encrypted_secret_key")
        if encrypted_secret_key:
            decrypted_secret_key = decrypt_secret_key(
                encrypted_secret_key, shopify_store_id, company_data.get("name"))
            company_data["secret_key"] = decrypted_secret_key
        return Partner(**company_data)
    return None

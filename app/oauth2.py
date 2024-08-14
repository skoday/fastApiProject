import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app import schemas, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/")


SECRET_KEY = "cd1ad3b15b27962062fbe3e5ab504c076cc9132c66aa2487da5e67bb2495563e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
        return token_data
    except jwt.PyJWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.Users | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    """
    Theoretically, this function might fetch the user from the db that way we can attach
    the user object to the request object. For now, we are just verifying the token.
    """
    token_data = verify_access_token(token, credentials_exception)
    user = db.get(models.Users, token_data.user_id)
    return user

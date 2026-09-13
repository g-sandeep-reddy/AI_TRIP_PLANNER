import os

from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)


def create_access_token(username):
    token = jwt.encode(
        {"sub": username},
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token):

    payload = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload["sub"]
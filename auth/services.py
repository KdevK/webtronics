# to hash password
import aiohttp
from passlib.context import CryptContext

from data.models import UserLoginSchema
from data.methods import get_user

from decouple import config

API_KEY = config("hunter_api_key")


async def get_password_hash(password: str) -> str:
    """
    Get hash from password

    :param password: password to hash
    :return: Hashed password
    """
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check whether the passwords match

    :param plain_password: password from form
    :param hashed_password: password from DB
    :return: true if passwords match else false
    """
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain_password, hashed_password)


async def check_user(data: UserLoginSchema):
    """
    Check whether user's passwords match

    :param data: user from session
    :return: true if passwords match else false
    """
    user = get_user(data.email)
    if user:
        if await verify_password(data.password, user.password):
            return True
    return False


async def check_email(email_address):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.hunter.io/v2/email-verifier?email={email_address}&api_key={API_KEY}"
        async with session.get(url) as resp:
            email_json = await resp.json()
            if email_json["data"]["status"] != "invalid":
                return True
            return False

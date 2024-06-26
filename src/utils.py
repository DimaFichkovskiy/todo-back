import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"


async def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


# import jwt
# from src.config import Config


# class VerifyToken:
#     def __init__(self, token):
#         self.token = token
#         self.config = Config
#         self.signing_key = None
#
#         jwks_url = f'https://{self.config.set_up_auth0()["DOMAIN"]}/.well-known/jwks.json'
#         self.jwks_client = jwt.PyJWKClient(jwks_url)
#
#     async def verify_token_from_auth0(self):
#         try:
#             self.signing_key = self.jwks_client.get_signing_key_from_jwt(self.token).key
#
#         except jwt.exceptions.PyJWKClientError as error:
#             return {"status": "error", "msg": error.__str__()}
#
#         except jwt.exceptions.DecodeError as error:
#             return {"status": "error", "msg": error.__str__()}
#
#         try:
#             payload = jwt.decode(
#                 self.token,
#                 self.signing_key,
#                 algorithms=self.config.set_up_auth0()["ALGORITHMS"],
#                 audience=self.config.set_up_auth0()["API_AUDIENCE"],
#                 issuer=self.config.set_up_auth0()["ISSUER"],
#             )
#         except Exception as e:
#             return {"status": "error", "message": str(e)}
#
#         return payload
#
#     async def verify_token_from_me(self):
#         try:
#             payload = jwt.decode(
#                 self.token,
#                 self.config.SECRET_KEY,
#                 algorithms=[self.config.ENCODE_ALGORITHM]
#             )
#         except Exception as e:
#             return {"status": "error", "message": str(e)}
#
#         return payload

import os
import secrets
from dotenv import load_dotenv
from configparser import ConfigParser

BASEDIR = os.path.abspath(os.path.dirname("../"))
load_dotenv(dotenv_path=f"{BASEDIR}/.env")


class Config:
    MONGO_DB_URL: str = os.getenv("MONGO_DB_URL")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ENCODE_ALGORITHM: str = os.getenv("JWT_ENCODE_ALGORITHM")
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")

    @staticmethod
    def set_up_auth0() -> dict:

        env = os.getenv("ENV", f"{BASEDIR}/.config")

        if env == ".config":
            config = ConfigParser()
            config.read(".config")
            config = config["AUTH0"]
        else:
            config = {
                "DOMAIN": os.getenv("DOMAIN"),
                "API_AUDIENCE": os.getenv("API_AUDIENCE"),
                "ISSUER": os.getenv("ISSUER"),
                "ALGORITHMS": os.getenv("ALGORITHMS"),
                "CLIENT_ID": os.getenv("CLIENT_ID"),
                "CLIENT_SECRET": os.getenv("CLIENT_SECRET"),
                "CONNECTION": os.getenv("CONNECTION")
            }
        return config

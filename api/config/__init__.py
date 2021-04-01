from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = 'foodieFOX Authentication'
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 5000


class DatabaseSettings(BaseSettings):
    REALM_APP_ID: str
    DB_NAME: str
    DB_URL: str


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    SECURE_COOKIE: bool = False


class Settings(CommonSettings, ServerSettings, DatabaseSettings, AuthSettings):
    pass


settings = Settings()

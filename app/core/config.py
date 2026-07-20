from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    SECRET_KEY: str
    DATABASE_URL: str
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_USERNAME: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
from pydantic import BaseSettings

class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRATION_MIN: int
    # REFRESH_TOKEN_EXPIRATION_MIN: int
    # JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"

def get_envs():
    return Settings()
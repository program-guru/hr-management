from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These attributes will automatically be populated from the .env file
    DATABASE_URI: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256" # Providing a default value
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # Providing a default value

    # This tells Pydantic where to find the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Global instance of the settings to import elsewhere
settings = Settings()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./inventory.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google OAuth Settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_CONF_URL: str = 'https://accounts.google.com/.well-known/openid-configuration'
    GOOGLE_REDIRECT_URI: str = "http://localhost:9000/api/auth/callback"  # Match Google Console

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

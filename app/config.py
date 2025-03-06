from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./inventory.db"
    # SECRET_KEY: str = "your-very-secure-secret-key-here-32-characters-long"
    SECRET_KEY:str="8273d3364e7c54288c5a66e5d478debb13dbc18ff91e7fe6446575fad36a76318cfb02ca11e01bfc7345e5d373eb444d15cf460b8f209838f8a71ccc8dfb7008f49ea5f68db2cd8cdbae67a9d58972e44d267d189a54f67579e6a744c8de5ee010923692fc6105c292436a281dc32513131e676a44b43e4b730db65f336724da5e4c78a8968fa1912d44a4b2cc592d1fd9bfd9d95fbc007b76d478356eda75e92b68ca03199e3a4b2a3a0e3cc30c89d96341d0c8df6478ddda4654a7981a532a"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


    GOOGLE_CONF_URL: str = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_CLIENT_ID: str = "your-google-client-id"
    GOOGLE_CLIENT_SECRET: str = "your-google-client-secret"
    GOOGLE_REDIRECT_URI: str = "http://localhost:9000/auth/callback"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()

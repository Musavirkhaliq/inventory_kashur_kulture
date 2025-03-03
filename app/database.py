# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from contextlib import contextmanager
# import logging

# logger = logging.getLogger(__name__)

# class Settings:
#     DATABASE_URL = "sqlite:///./inventory.db"
#     POOL_SIZE = 5
#     MAX_OVERFLOW = 10

# settings = Settings()

# try:
#     engine = create_engine(
#         settings.DATABASE_URL,
#         pool_size=settings.POOL_SIZE,
#         max_overflow=settings.MAX_OVERFLOW,
#         connect_args={"check_same_thread": False}  # Only for SQLite
#     )
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     Base = declarative_base()
# except Exception as e:
#     logger.error(f"Failed to initialize database: {str(e)}")
#     raise

# @contextmanager
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     except Exception as e:
#         logger.error(f"Database error: {str(e)}")
#         db.rollback()
#         raise
#     finally:
#         db.close()


from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL  

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
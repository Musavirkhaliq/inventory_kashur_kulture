# 2. **`database.py`**:
#    - **Purpose**: Initializes the database connection and creates a session factory.
#    - **Key Components**:
#      - `SQLALCHEMY_DATABASE_URL`: Specifies the database URL (SQLite in this case).
#      - `engine`: Creates the database engine.
#      - `SessionLocal`: Creates a session factory for database interactions.
#      - `Base`: Base class for SQLAlchemy models.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./inventory.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
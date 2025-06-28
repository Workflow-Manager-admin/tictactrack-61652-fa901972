import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

from .models import Base

# Load environment variables from .env if available
load_dotenv()

DB_CONNECTION_STRING = os.getenv(
    "TICTACTOE_DB_URL",
    "sqlite:///./tic_tac_toe.db"
)  # Default to SQLite for dev

# Create SQLAlchemy engine
engine = create_engine(
    DB_CONNECTION_STRING,
    connect_args={"check_same_thread": False}
    if "sqlite" in DB_CONNECTION_STRING else {}
)

# PUBLIC_INTERFACE
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


# PUBLIC_INTERFACE
def init_db():
    """
    Initialize database models (create tables).
    Call this at startup to ensure all tables exist.
    """
    Base.metadata.create_all(bind=engine)

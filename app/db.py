from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for model declarations
Base = declarative_base()

def get_db():
    """
    Dependency generator for FastAPI that yields a database session.
    Closes the session after request is handled.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

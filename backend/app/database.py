from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DB_URL

engine = create_engine(
    DB_URL, 
    echo=True,
    pool_pre_ping=True,
    pool_recycle=280,
    pool_size=10,
    max_overflow=5
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
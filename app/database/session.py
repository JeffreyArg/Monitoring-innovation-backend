from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import configs

engine = create_engine(
    configs.DATABASE_URL,
    echo=True,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

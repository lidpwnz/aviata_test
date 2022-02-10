import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

DB_URL = f'postgresql://postgres:postgres@db:5432/postgres'

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

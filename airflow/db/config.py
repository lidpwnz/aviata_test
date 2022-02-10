import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

DB_URL = f'postgresql://{user}:{password}@{host}:{port}/{db}'

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

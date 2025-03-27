from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

host = environ["POSTGRES_HOST"]
port = environ["POSTGRES_PORT"]
user = environ["POSTGRES_USER"]
password = environ["POSTGRES_PASSWORD"]
db = environ["POSTGRES_DB"]
dbtype = "postgresql"

SQLALCHEMY_DATABASE_URI = f"{dbtype}://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

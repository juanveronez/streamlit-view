from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base

import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.prod')

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine: Engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_database():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine, false
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = "postgresql://postgres:postgres@localhost:5432/Techholding"

engine = create_engine(URL)
Session = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
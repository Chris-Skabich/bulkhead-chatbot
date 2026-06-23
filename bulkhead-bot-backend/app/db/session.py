# Postgres connection logic
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


#Pull the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the core database engine
engine=create_engine(DATABASE_URL, echo=True)

# Create a session factory for handling querys
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base Class for our database models
Base = declarative_base()

#dependancy to get a DB Session per API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


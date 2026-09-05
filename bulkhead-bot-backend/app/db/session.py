# Postgres connection logic
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


#Pull the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please set it in your .env file.")

# Create the core database engine
engine=create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a session factory for handling queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base Class for our database models
Base = declarative_base()

# Dependancy to get a DB Session per API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


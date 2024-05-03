from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Postgresql connection
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@db/postgres"

# Create a Postgresql engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create declarative base meta instance
Base = declarative_base()

# Create session local class for sessio maker
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


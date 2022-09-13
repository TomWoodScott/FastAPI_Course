from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create engine
SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog.db'
engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread":False})


# create session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# create mapping
Base = declarative_base()
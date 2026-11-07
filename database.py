from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session

url = "sqlite:///./task.db"
engine = create_engine(url)
session = sessionmaker(bind=engine, autoflush=True)

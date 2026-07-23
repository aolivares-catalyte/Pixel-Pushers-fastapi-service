from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine 

engine = create_engine("sqlite:///database.db", echo=True)

class Base(DeclarativeBase):
    pass



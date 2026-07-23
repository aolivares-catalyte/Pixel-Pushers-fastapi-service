from sqlalchemy import DeclarativeBase, create_engine

engine = create_engine("sqlite:///database.db", echo=True)

class Base(DeclarativeBase):
    pass



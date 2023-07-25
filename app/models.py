from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = Column(Integer)

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

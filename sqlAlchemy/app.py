from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# engine = create_engine('postgresql://Nath:1234@localhost:5432/flaskAPI')
engine = create_engine('sqlite:///bdd.db')
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


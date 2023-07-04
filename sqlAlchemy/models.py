# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from config import engine, Base
from app import db
from app import app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

with app.app_context():
    db.create_all()

# class Role(Base):
#     __tablename__ = 'role'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
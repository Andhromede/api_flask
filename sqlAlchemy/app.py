from sqlalchemy.orm import sessionmaker
from flask import Flask, request, jsonify
from config import engine, Base
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bdd.db'

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
db = SQLAlchemy(app)
from models import User


@app.route("/users", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            password=request.form["password"],
            email=request.form["email"],
            id=request.form["id"]
        )
        db.session.add(user)
        db.session.commit()
        return 'Utilisateur créé avec succès', 201
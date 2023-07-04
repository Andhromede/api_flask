from sqlalchemy.orm import sessionmaker
from flask import Flask, request, jsonify
from config import engine, Base
from flask_sqlalchemy import SQLAlchemy
from models import User, Role


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bdd.db'

# engine = create_engine('postgresql://Nath:1234@localhost:5432/flaskAPI')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
db = SQLAlchemy(app)
db.init_app(app)


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
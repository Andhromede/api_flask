from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import User


# APP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Nath:1234@localhost:5432/flaskAPI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# END POINTS
@app.route('/create_table')
def create_table():
    db.create_all()
    return 'Tables créées'
# db.create_all()


@app.route('/api/users')
def get_users():
    users = User.query.all()
    return jsonify(users)


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    password = data['password']
    email = data['email']

    new_user = User(password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'})





if __name__ == '__main__':
    app.run()
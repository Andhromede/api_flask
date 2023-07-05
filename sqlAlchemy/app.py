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
from models import User, Role, Article
with app.app_context():
    db.create_all()


# ======================================= USER CRUD =======================================

""" GET/POST USER
    GET Returns: a List of users
    POST Returns: a string
    _type_: post or get user(s)
"""
@app.route("/user", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            id=request.form["id"],
            email=request.form["email"],
            password=request.form["password"],
            role_id=request.form["role"]
        )
        db.session.add(user)
        db.session.commit()
        return 'Utilisateur créé avec succès', 201

    if request.method == "GET":
        users = User.query.all()
        result = []

        for user in users:
            role = Role.query.get(user.role_id)
            user_role=({'id': role.id, 'name': role.name})
            result.append({'id': user.id, 'email': user.email, 'password': user.password, 'role': user_role})
        
        return jsonify(result)

""" GET USER BY ID
    Returns: a USER 
    _type_: get a USER by ID
"""
@app.route("/user/<int:id>", methods=["GET"])
def user_id(id):
    user = User.query.get(id)
    if user:
        role = Role.query.get(user.role_id)
        user_role = ({'id': role.id, 'name': role.name})
        return jsonify({'id': user.id, 'email': user.email, 'password': user.password, 'role': user_role})
    else:
        return 'Role non trouvé', 404

""" UPDATE USER
    Returns: a user
    _type_: update a user by id
"""
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user:
        user.email = request.form['email']
        user.password = request.form['password']
        user.role_id = request.form['role']
        db.session.commit()

        role = Role.query.get(user.role_id)
        user_role = ({'id': role.id, 'name': role.name})
        new_user = jsonify({'id': user.id, 'email': user.email, 'password': user.password, 'role': user_role})
        return new_user
    else:
        return 'Utilisateur non trouvé', 404

""" DELETE USER BY ID
    Returns: a string
    _type_: DELETE a USER by ID
"""
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'Utilisateur supprimé avec succès', 200
    else:
        return 'Utilisateur non trouvé', 404


# ======================================= ROLE CRUD =======================================

""" GET/POST ROLE
    GET Returns: a List of roles
    POST Returns: a string
    _type_: post or get role(s)
"""
@app.route("/role", methods=["GET", "POST"])
def role_create():
    if request.method == "POST":
        role = Role(
            id=request.form["id"],
            name=request.form["name"]
        )
        db.session.add(role)
        db.session.commit()
        return 'Role créé avec succès', 201
    
    if request.method == "GET":
        roles = Role.query.all()
        result = []
        for role in roles:
            result.append({'id': role.id, 'name': role.name})
        return jsonify(result)

""" GET ROLE BY ID
    Returns: a role 
    _type_: get a role by ID
"""
@app.route("/role/<int:id>", methods=["GET"])
def role_id(id):
    role = Role.query.get(id)
    if role:
        return jsonify({'id': role.id, 'name': role.name})
    else:
        return 'Role non trouvé', 404

""" UPDATE ROLE
    Returns: a role
    _type_: update a role by id
"""
@app.route('/role/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get(id)
    if role:
        role.name = request.form['name']
        db.session.commit()
        role = jsonify({'id': role.id, 'name': role.name})
        return role
    else:
        return 'Role non trouvé', 404

""" DELETE ROLE BY ID
    Returns: a string
    _type_: DELETE a ROLE by ID
"""
@app.route('/role/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get(id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return 'Role supprimé avec succès', 200
    else:
        return 'Role non trouvé', 404


# ======================================= ARTICLE CRUD =======================================

""" GET/POST ARTICLE
    GET Returns: a List of articles
    POST Returns: a string
    _type_: post or get article(s)
"""
@app.route("/article", methods=["GET", "POST"])
def article_create():
    if request.method == "POST":
        article = Article(
            id = request.form["id"],
            title = request.form["title"],
            text = request.form["text"],
            user_id = request.form["user_id"]
        )
        db.session.add(article)
        db.session.commit()
        return 'Article créé avec succès', 201

    if request.method == "GET":
        articles = Article.query.all()
        result_article = []

        for article in articles:
            user = User.query.get(article.user_id)
            role = Role.query.get(user.role_id)
            role_user = ({'id': role.id, 'name': role.name })
            user_article = ({'id': user.id, 'email': user.email, 'password': user.password, 'role':role_user })
            result_article.append({'id': article.id, 'email': article.title, 'text': article.text, 'user': user_article })
        return jsonify(result_article)

""" GET USER BY ID
    Returns: a USER 
    _type_: get a USER by ID
"""
@app.route("/article/<int:id>", methods=["GET"])
def article_id(id):
    article = Article.query.get(id)
    
    if article:
        user = User.query.get(article.user_id)
        role = Role.query.get(user.role_id)
        role_user = ({'id': role.id, 'name': role.name })
        user_article = ({'id': user.id, 'email': user.email, 'password': user.password, 'role': role_user })
        result_article = ({'id': article.id, 'email': article.title, 'text': article.text, 'user': user_article })
        
        return jsonify(result_article)
    else:
        return 'Role non trouvé', 404
    
""" UPDATE ARTICLE
    Returns: a article
    _type_: update a article by id
"""
@app.route('/article/<int:id>', methods=['PUT'])
def update_article(id):
    article = Article.query.get(id)
    if article:
        article.title = request.form['title']
        article.text = request.form['text']
        article.user_id = request.form['user_id']
        db.session.commit()

        user = User.query.get(article.user_id)
        role = Role.query.get(user.role_id)
        role_user = ({'id': role.id, 'name': role.name })
        user_article = ({'id': user.id, 'email': user.email, 'password': user.password, 'role': role_user })
        result_article = ({'id': article.id, 'email': article.title, 'text': article.text, 'user': user_article })
        return result_article
    else:
        return 'article non trouvé', 404

""" DELETE ARTICLE BY ID
    Returns: a string
    _type_: DELETE a ARTICLE by ID
"""
@app.route('/article/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Article.query.get(id)
    if article:
        db.session.delete(article)
        db.session.commit()
        return 'Article supprimé avec succès', 200
    else:
        return 'Articme non trouvé', 404






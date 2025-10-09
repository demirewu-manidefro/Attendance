from flask import Flask
from flask_bcrypt import Bcrypt
from db import db
from models import User  # or Employee if you use Employee table

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://myuser:mypassword@localhost/mydb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    # Example: create a new user with a password
    username = input("Enter username: ")
    raw_password = input("Enter password: ")

    hashed_pw = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    user = User(username=username, password=hashed_pw)  # make sure your User model has a password field
    db.session.add(user)
    db.session.commit()

    print(f"User {username} created with hashed password!")

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:ahati21+@localhost:5432/attendance_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

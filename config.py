# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/fitness_center'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'

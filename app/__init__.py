from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config['SECRET_KEY']='be951dcde0aa8ef79d522fe7f3e9e396'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)

from app import routes

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app=Flask(__name__)

app.config['SECRET_KEY']=os.environ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USERNAME']=os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD']=os.environ['MAIL_PASSSWORD']


mail=Mail(app)



from app.users.routes import users
from app.main.routes import main
from app.posts.routes import posts
from app.tags.routes import tags

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(tags)

from app.models import User, Post

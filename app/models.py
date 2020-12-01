from datetime import datetime
from app import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True,nullable=False)
    email=db.Column(db.String(120), unique=True,nullable=False)
    image_file=db.Column(db.String(20), nullable=False,default='default.jpeg')
    password=db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s=Serializer(app.config['SECRET_KEY'], expires_sec)
        token=s.dumps({'user_id':self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(app.config['SECRET_KEY'])
        try:
            s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)




    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}' )"


class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    created_at=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary='post_tag', lazy='dynamic', back_populates='posts')

    def __repr__(self):
        return f"Post('{self.title}', '{self.created_at}')"


class Tag(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    value=db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', secondary='post_tag', lazy='dynamic', back_populates='tags')
    def __repr__(self):
        return f"Tag('{self.value}')"


# many-to-many association table: blog_post - blog_tag
post_tag_table = db.Table('post_tag', db.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)
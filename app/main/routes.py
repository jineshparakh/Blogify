from flask import Blueprint, render_template, request
from app.models import Post

main=Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page=request.args.get('page', default=1, type=int)
    posts=Post.query.order_by(Post.created_at.desc()).paginate(per_page=3, page=page)
    return render_template('home.html', posts=posts, featPost = posts.items[0])


@main.route('/about')
def  about():
    return render_template('about.html',title='About')
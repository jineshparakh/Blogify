from app.tags.forms import TagForm
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from werkzeug.utils import html
from app import db
from app.models import Post, Tag
from app.posts.forms import PostForm
import markdown

posts=Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    tagForm = TagForm()
    tags=Tag.query.all()
    form.tags.choices = [(tag.id, tag.value) for tag in tags]
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=repr(form.content.data), author=current_user, tags=Tag.query.filter(Tag.id.in_(form.tags.data)).all())
        db.session.add(post)
        db.session.commit()
        flash(f'Your Post has been created!!', category='success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post',legend='New Post', form=form, tags=tags, tagForm=tagForm)


@posts.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=PostForm()
    tagForm = TagForm()
    tags=Tag.query.all()
    form.tags.choices = [(tag.id, tag.value) for tag in tags]
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=repr(form.content.data)
        post.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        db.session.commit()
        flash(f'Your Post has been updated!!', category='success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
        selectedTags=post.tags 
        return render_template('create_post.html', title='Update Post', legend='Update Post', form=form, tags=tags, tagForm=tagForm, selectedTags=selectedTags)
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form, tags=tags, tagForm=tagForm)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your Post has been deleted!!', category='success')
    return redirect(url_for('main.home'))
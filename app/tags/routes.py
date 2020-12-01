from flask import Blueprint, url_for, flash, redirect, render_template, request
from flask_login import current_user, login_required
from werkzeug.utils import html
from app import db
from app.models import Tag, PostTag, Post
from app.tags.forms import TagForm

tags=Blueprint('tags', __name__)

@tags.route('/tags/new', methods=['POST'])
@login_required
def new_tag():
    tagForm=TagForm()
    if tagForm.validate_on_submit():
        tag=Tag(value=tagForm.value.data.upper())
        try:
            db.session.add(tag)
            db.session.commit()
            flash(f'Tag has been created!!', category='success')
            return redirect(url_for('posts.new_post'))
        except:
            flash(f'Tag Already Exists', category='warning')
            return redirect(url_for('posts.new_post'))    
    flash(f'Could not create tag. Something went wrong.', category='error')
    return redirect(url_for('posts.new_post'))


@tags.route('/tags/<string:selectedTag>')
@login_required
def searchPostsViaTag(selectedTag):
    tagId=Tag.query.filter_by(value=selectedTag).first_or_404().id
    print(tagId)
    allPostsWithGivenTag=PostTag.query.filter_by(tag_id=tagId).all()
    postIds=[post.post_id for post in allPostsWithGivenTag]
    print(postIds)
    page=request.args.get('page', default=1, type=int)
    posts=Post.query.filter(Post.id.in_(postIds)).order_by(Post.created_at.desc()).paginate(page=page, per_page=3)
    print(posts)
    print(allPostsWithGivenTag)
    return render_template('tagged_posts.html', posts=posts, tag=selectedTag)



    print(selectedTag)
    return '<h1>selectedTag</h1>'


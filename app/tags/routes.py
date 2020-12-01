from flask import Blueprint, url_for, flash, redirect
from flask_login import current_user, login_required
from werkzeug.utils import html
from app import db
from app.models import Tag
from app.tags.forms import TagForm

tags=Blueprint('tags', __name__)

@tags.route('/tags/new', methods=['POST'])
@login_required
def new_tag():
    tagForm=TagForm()
    if tagForm.validate_on_submit():
        tag=Tag(value=tagForm.value.data)
        db.session.add(tag)
        db.session.commit()
        flash(f'Tag has been created!!', category='success')
        return redirect(url_for('posts.new_post'))
    flash(f'Could not create tag. Something went wrong.', category='error')
    return redirect(url_for('posts.new_post'))



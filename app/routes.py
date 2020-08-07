import os
from flask import render_template, flash, redirect, request,url_for, abort
from app import app,db,bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user,login_required
import secrets
from PIL import Image #to resize large image files



@app.route('/')
@app.route('/home')
def home():
    page=request.args.get('page', default=1, type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template('home.html', posts=posts)


@app.route('/about')
def  about():
    return render_template('about.html',title='About')

@app.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect('home')
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user= User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Account Created for {form.username.data}!, you can now login :)', category='success')
            return redirect('login')
        except:
            flash(f'The user is already registered!! Try to login!!', category='danger')    
        

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect('home')
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            flash(f'Hey {user.username}! Good to see you back ;)', category='success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('home')    
        else:
            flash(f'Login Unsuccessful. Please check the email and/or Password', 'danger')  
              
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('home')

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_filename=random_hex+f_ext
    picture_path=os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename



@app.route('/account', methods=['POST','GET'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash(f'Account Details Updated!!', category='success')
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email    
    image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form)



@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your Post has been created!!', category='success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',legend='New Post', form=form)


@app.route('/post/<int:post_id>')  
def post(post_id):
    post=Post.query.get_or_404(post_id)  
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])  
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash(f'Your Post has been updated!!', category='success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method=='GET':    
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)


@app.route('/post/<int:post_id>/delete', methods=['POST'])  
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your Post has been deleted!!', category='success')
    return redirect(url_for('home'))
          

@app.route('/user/<string:username>')
def user_posts(username):
    page=request.args.get('page', default=1, type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts,user=user)







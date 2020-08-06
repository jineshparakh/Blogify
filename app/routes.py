import os
from flask import render_template, flash, redirect, request,url_for
from app import app,db,bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user,login_required
import secrets
from PIL import Image



posts =[
    {
        'author':'Jinesh',
        'title':'Blog Post 1',
        'content':'First Post Content',
        'date_posted':'July 31, 2020'
    },
    {
        'author':'Pushkar',
        'title':'Blog Post 2',
        'content':'Second Post Content',
        'date_posted':'July 31, 2020'
    }
]

@app.route('/')
@app.route('/home')
def home():
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
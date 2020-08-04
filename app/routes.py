from flask import render_template, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post


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
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', category='success')
        return redirect('home')

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash(f'Login Successful for {form.email.data}!', category='success')
        return redirect('home')
    else:
        flash(f'Login Unsuccessful. Please check the Username and/or Password', 'danger')    
    return render_template('login.html', title='Login', form=form)





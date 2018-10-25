from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User, Opinion, Book
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, AddBookForm


@app.route('/')
@app.route('/index')
#@login_required
def index():
    posts = Opinion.query.all()
	# user = {'username': 'User'}
	# posts = [
 #        {
 #            'author': {'username': 'Example 1'},
 #            'body': 'Going to develop this site!'
 #        },
 #        {
 #            'author': {'username': 'Example 2'},
 #            'body': 'Still learning!'
 #        }
 #    ]
    
    return render_template('index.html', title='Home', posts=posts)   #,posts=posts) return site's view


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/show_books', methods=['GET', 'POST'])
def show_books():
    books = Book.query.all()
    return render_template('books.html', title='Home', books=books)




@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if current_user.is_authenticated:
        form = AddBookForm()
        if form.validate_on_submit():
            added_book = Book(title=form.title.data, description=form.description.data)
            db.session.add(added_book)
            db.session.commit()
            flash('Book has been added')
            return redirect(url_for('show_books'))

        return render_template('add_books.html', title='Add Book', form=form)
    return redirect(url_for('login'))    



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

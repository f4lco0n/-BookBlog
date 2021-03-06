from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User, Opinion, Book, Category
from flask_login import login_required
from flask import request, make_response
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, AddBookForm
from sqlalchemy import and_


@app.route('/')
@app.route('/index')
def index():
    posts = Opinion.query.all()

    return render_template('index.html', title='Home', posts=posts) 


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
        login_user(user)
        
        userCookie = request.form['username']
        resp = make_response(render_template('index.html'))
        resp.set_cookie('user', userCookie)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return resp
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form) 


@app.route('/show_books', methods=['GET', 'POST'])
def show_books():
    books = Book.query.all()
    return render_template('books.html', title='Books', books=books)


@app.route('/detail_book/<title>')
def detail_book(title):
    book = Book.query.filter_by(title=title).first_or_404()
    result = db.session.query(Book.id, Opinion.body).filter(Opinion.book_id==book.id).filter(and_(Book.title == title)).all()
    return render_template('detail_book.html', book=book, result=result)



@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if current_user.is_authenticated:
        form = AddBookForm()
        if form.validate_on_submit():
            added_book = Book(title=form.title.data, description=form.description.data,
                            author=form.author.data, pages=form.pages.data)
            db.session.add(added_book)
            db.session.commit()
            return redirect(url_for('show_books'))

        return render_template('add_books.html', title='Add Book', form=form)
    return redirect(url_for('login'))    



@app.route('/logout')
def logout():
    logout_user()
    resp = make_response(redirect('/index'))
    resp.delete_cookie('user')
    return resp
    #return redirect(url_for('index'))

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

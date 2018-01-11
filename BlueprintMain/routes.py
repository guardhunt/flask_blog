from flask import Blueprint, render_template, abort, url_for, redirect, flash
from jinja2 import TemplateNotFound
from sqlalchemy.orm import Query
from models import Posts, Users
from flask_login import current_user, login_user
from forms.login import LoginForm

main = Blueprint('main', __name__, template_folder='../templates', static_folder='../static')


@main.route('/')
def index():
    try:
        links = [{'href': 'http://www.google.com', 'caption': '/Index'},
                 {'href': 'http://www.bitbucket.com', 'caption': '/Talk'}]
        return render_template('base.html', check_var='Testing This Variable', nav=links)
    except TemplateNotFound:
        abort(404)


@main.route('/blog')
def blog():
    posts = Posts.query.filter_by(published=True)
    return render_template('blog.html', posts=posts)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

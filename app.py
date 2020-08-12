import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Follows, Comment, Post, Ingredient, Cabinet, CabinetIngredient
from forms import UserAddForm, LoginForm

#blueprints
from blueprints.user.user import user
from blueprints.cabinet.cabinet import cabinet
from blueprints.cdb.cdb import cdb

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(cabinet, url_prefix="/cabinet")
app.register_blueprint(cdb, url_prefix = "/api/cdb")

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///bartender'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
# Functions for Authorization Management
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


# home/ feed - requires authorization
@app.route('/')
def landing_page():
    #
    # shows feed for logged in users, landing page if no user
    #
    if g.user:
        return redirect('/user/')
    signup_form = UserAddForm()

    login_form = LoginForm()

    return render_template('landing_page.html', signup_form = signup_form, login_form = login_form )

# log in route - global access
@app.route('/login', methods=["POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/user/")

        flash("Invalid credentials.", 'danger')

        return redirect('/')
    else:
        return redirect('/')


# log out route - requires authorization
@app.route('/logout')
def log_out_user():
    """Handle logout of user."""

    do_logout()
    flash('Logged Out Successfully', 'success')

    return redirect('/')


@app.route('/signup', methods=['POST'])
def sign_up_user():

    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/user/")
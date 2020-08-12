from flask import Blueprint, render_template, g, flash, redirect, session
from models import User, Follows, db

user = Blueprint("user", __name__, template_folder="templates")

#ALL USEr ROUTES REQUIRE AUTH

@user.route('/')
def show_home():

    if g.user:
        return render_template('user/home.html')
    else:
        flash('Please Login', 'secondary')
        return redirect('/')

# /<username> - renders profile of other users
@user.route('/<username>')
def show_profile(username):

    user = User.query.filter(User.username == username).first()

    if user == g.user:
        flash('hello!')
        return render_template('user/edit_profile.html')

    elif user:
        flash(f'{user}')
        return render_template('user/profile.html')

    else:
        flash('Could not find that User.', 'warning')
        return redirect('/user')
# /cabinet - directs to cabinet blue print

@user.route('/request/<int:id>', methods= ['POST'])
def request_friend(id):

    # friend = User.query.get_or_404(id)

    # g.user.friends.append(friend)
    
    db.session.commit()
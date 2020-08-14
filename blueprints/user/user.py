from flask import Blueprint, render_template, g, flash, redirect, session, jsonify
from models import User, Follows, db, Cabinet, Post, Comment
from .forms import PostForm, CommentForm
from ..post.post import post

user = Blueprint("user", __name__, template_folder="templates", static_folder="static")
# user.register_blueprint(post, url_prefix="/post")
#ALL USEr ROUTES REQUIRE AUTH

@user.route('/')
def show_home():

    if g.user:
        following = [user.id for user in g.user.following]
        bartalk = Post.query.filter((Post.user_id == g.user.id) | (Post.user_id.in_(following))).order_by(Post.timestamp).all()
        return render_template('user/home.html', bartalk=bartalk)
    else:
        flash('Please Login', 'secondary')
        return redirect('/')

# /<username> - renders profile of other users
@user.route('/<username>')
def show_profile(username):

    user = User.query.filter(User.username == username).first()
    
    if user == g.user:
        # cabinet = Cabinet.query.filter(Cabinet.user_id == g.user.id).one_or_none()
        return render_template('user/edit_profile.html')

    elif user:
        # cabinet = Cabinet.query.filter(Cabinet.user_id == user.id).one_or_none()
        return render_template('user/profile.html', user = user)

    else:
        flash('Could not find that User.', 'warning')
        return redirect('/user')
# /cabinet - directs to cabinet blue print

@user.route('/follow/<int:id>', methods= ['GET','POST'])
def follow_user(id):
    """Add a follow for the currently-logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f'/user/{followed_user.username}')

@user.route('/create', methods=['GET','POST'])
def create_post():
    if not g.user:
        flash("Please Log In", "danger")
        return redirect("/")

    form = PostForm()

    if form.validate_on_submit():

        post = Post(content=form.content.data, user_id=g.user.id)

        db.session.add(post)
        db.session.commit()

        return redirect('/user')

    else:
        return render_template('user/post.html', form=form)

@user.route('/comment/<int:post_id>', methods=['GET','POST'])
def add_comment(post_id):
    if not g.user:
        flash("Please Log In", "danger")
        return redirect("/")

    form = CommentForm()
    post = Post.query.get_or_404(post_id)

    if form.validate_on_submit():

        comment = Comment(content=form.content.data, user_id=g.user.id, post_id=post_id)

        db.session.add(comment)
        db.session.commit()

        return redirect(f'/post/{post_id}')

    else:
        return render_template('user/comment.html', form = form, post=post)
from flask import Blueprint, render_template, g, flash, redirect, session
from models import Cabinet, CabinetIngredient, Ingredient, db, User, Post, Comment

post = Blueprint("post", __name__, template_folder="templates")

@post.route('/<int:post_id>')
def show_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post/post.html', post=post)
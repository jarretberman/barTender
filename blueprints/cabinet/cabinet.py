from flask import Blueprint, render_template, g, flash, redirect, session
from models import Cabinet, CabinetIngredient, Ingredient, db

cabinet = Blueprint("cabinet", __name__, template_folder="templates")

@cabinet.route('/')
def test():
    return 'TEST'

@cabinet.route('/add/<name>', methods= ['GET','POST'])
def add_to_cabinet(name):
    """Add ingredients to Cabinet"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    ingredient = Ingredient.query.filter(Ingredient.name == name).one_or_none()

    if ingredient:
        cabinet = Cabinet.query.filter(Cabinet.user_id == g.user.id).first()
        cabinet.ingredients.append(ingredient)
        db.session.commit()
        flash('Added Ingredient Successfully')
    else:
        flash('Could not find ingredient')

    return redirect('/user')

@cabinet.route('/remove', methods = ['POST'])
def remove_from_cabinet():
    """Remove ingredients from Cabinet"""

    return redirect('/cabinet')

@cabinet.route('/get')
def get_cabinet_list():
    """Returns Cabinet Info"""

    return redirect('/cabinet')
from flask import Blueprint, render_template, g, flash, redirect, session
from models import Cabinet, CabinetIngredient, Ingredient

cabinet = Blueprint("cabinet", __name__, template_folder="templates")

@cabinet.route('/')
def test():
    return 'TEST'

@cabinet.route('/add', methods= ['POST'])
def add_to_cabinet():
    """Add ingredients to Cabinet"""

    return redirect('/cabinet')

@cabinet.route('/remove', methods = ['POST'])
def remove_from_cabinet():
    """Remove ingredients from Cabinet"""

    return redirect('/cabinet')

@cabinet.route('/get')
def get_cabinet_list():
    """Returns Cabinet Info"""

    return redirect('/cabinet')
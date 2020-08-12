from flask import Blueprint, render_template, g, flash, redirect, session

cdb = Blueprint("cdb", __name__, template_folder="templates")
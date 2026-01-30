from flask import Blueprint, render_template

# create a blueprint (like a factory method)
# registered in __init__.py
bp = Blueprint('auth', __name__)

# @bp.route('/')
# def home():
#     return render_template('home.html')

# @bp.route('/')
# def 
from flask import Blueprint

mod = Blueprint('site', __name__)

@mod.route('/homepage')
def homepage():
    return '<h1>you are on the home page</h1>'
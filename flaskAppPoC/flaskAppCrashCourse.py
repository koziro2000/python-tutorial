# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 05:37:31 2018

@author: jroh
"""

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'

class LoginForm(FlaskForm):
    username = StringField('username', validators=\
                           [InputRequired(message='A user name is required'),\
                            Length(min=5, max=10, message='Must be between 5 and 10')])
    password = PasswordField('password',  validators=[InputRequired('A password is required')])

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    
    if form.validate_on_submit():
        return '<h1>The user name is {}. The password is {}.'.format(\
                                     form.username.data, form.password.data)
    
    return render_template('form.html', form=form)
    
if __name__ == '__main__':
    app.run(debug=True)
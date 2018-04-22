# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 05:37:31 2018

#TODO:

    1. Navigation
    2. Authentication/Authorization
    3. Display various parts - create at least one page from POC
    4. Multi sessions
    5. 

@author: jroh
"""



import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, AnyOf


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['TESTING'] = True
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

anyOfPasswords = ['password', 'secret']

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='A user name is required'),Length(min=5, max=10, message='Must be between 5 and 10')])
    password = PasswordField('password',  validators=[InputRequired('A password is required'), AnyOf(values=anyOfPasswords)])
    

    
class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image only!')\
                                  , FileRequired(u'File was empty!')])   
    submit = SubmitField(u'Upload')
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
    else:
        file_url = None
    return render_template('fileUpload.html', form=form, file_url=file_url)
@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    
    if form.validate_on_submit():
        return '<h1>The user name is {}. The password is {}.'.format(\
                                     form.username.data, form.password.data)
    
    return render_template('form.html', form=form)
    
if __name__ == '__main__':
    app.run(debug=True)
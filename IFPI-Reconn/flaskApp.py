# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 12:41:35 2018

@author: jroh
"""

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}
    
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
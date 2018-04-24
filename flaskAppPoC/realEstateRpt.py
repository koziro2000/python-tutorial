"""
    this PoC is to constrcut those screens for RE
"""

"""
    General Partner Information


    {
        "Property":"Westfield Topanga",
        "Portfolio":"Westfield JV",
        "Property Type": "Super Regional Mall",
        "Acquisition Date": "March 2012",
        "Stabilization Date": "March 2012",
        "Year Built/Last Renovated": "1965/2008",
        "Location":"Los Angeles, CA",
        "NRA/GLA/Units":"1,554,776",
        "Lifecycle":"Operating - Near term renovation required",
        "Ownership Type":"Minority JV Interest",
        "CPPIB Ownership (%)":"45%",
        "Ground Lease (Expiration, Options)":"N/A"
    }


{"_id":"5ade917d88e80b2420fe3685","property":"westfield topanga","portfolio":"westfield JV","Property Type":"Super Regional Mall","Acquisition Date":"March 2012","Stabilization Date":"March 2012","Year Built/Last Renovated":"1965/2008","Location":"Los Angeles, CA","NRA/GLA/Units":"1,554,776","Lifecycle":"Operating - Near term renovation required","Ownership Type":"Minority JV Interest","CPPIB Ownership (%)":"45%","Ground Lease (Expiration, Options)":"N/A"}

"""

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm

client = MongoClient('localhost', 27017)
db = client.conquer
generalPartners = db.GeneralPartner

app = Flask(__name__)
title = "General Partner Information"
heading = "Asset Strategic Review"

@app.route("/")
def showGeneralPartner():
    generalPartnerSet = generalPartners.find_one()
    return render_template('showGeneralPartner.html', generalPartner = generalPartnerSet, t=title, h=heading)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
# Careful with the debug mode..

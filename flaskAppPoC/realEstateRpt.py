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
        "Ground Lease (Expiration, Options)":"N/A",
        "IRR Since Inception":"10.0% unlevered",
        "Long-Term Outlook/Strategy":"Positioned for long term growth",
        "Hold/Sell":"Hold",
        "Target Timing of Sale":"N/A",
        "Asset Liquidity(Market)":"Medium",
        "REI interest Liquidity(Market)":"Low",
        "Original GAV at 100%":"$1.0",
        "Original GAV at Share":"$0.5",
        "Current GAV at 100%":"$1.0",
        "Current GAV at Share":"$0.5",        
        "Current Total Cost Basis at 100%":"$1.0",
        "Current Total Cost Basis at Share":"$0.5",
        "Invested Equity at 100%":"$1.0",
        "Invested Equity at Share":"$0.5",
        "Current ECV at 100%":"$1.0",
        "Current ECV at Share":"$0.5"
    }

test

{"_id":"5ade917d88e80b2420fe3685","property":"westfield topanga","portfolio":"westfield JV","Property Type":"Super Regional Mall","Acquisition Date":"March 2012","Stabilization Date":"March 2012","Year Built/Last Renovated":"1965/2008","Location":"Los Angeles, CA","NRA/GLA/Units":"1,554,776","Lifecycle":"Operating - Near term renovation required","Ownership Type":"Minority JV Interest","CPPIB Ownership (%)":"45%","Ground Lease (Expiration, Options)":"N/A","IRR Since Inception":"10.0% unlevered","Long-Term Outlook/Strategy":"Positioned for long term growth","Hold/Sell":"Hold","Target Timing of Sale":"N/A","Asset Liquidity(Market)":"Medium","REI interest Liquidity(Market)":"Low","Original GAV at 100%":"$1.0","Original GAV at Share":"$0.5","Current GAV at 100%":"$1.0","Current GAV at Share":"$0.5","Current Total Cost Basis at 100%":"$1.0","Current Total Cost Basis at Share":"$0.5","Invested Equity at 100%":"$1.0","Invested Equity at Share":"$0.5","Current ECV at 100%":"$1.0","Current ECV at Share":"$0.5"}

"""
import json
import requests
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask import request
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client.conquer
generalPartners = db.GeneralPartner

app = Flask(__name__)
title = "General Partner Information"
heading = "Asset Strategic Review "

@app.route("/")
def showGeneralPartner():
    generalPartnerSet = generalPartners.find()
    return render_template('generalPartnerForm.html', generalPartners = generalPartnerSet, t=title, h=heading)

#This is for update button
@app.route("/update", methods = ['POST'])
def updateGeneralPartner():
    id = request.form['_id']

    requestData = request.form.to_dict(flat=False)
    print(requestData)

    generalPartnerSet = generalPartners.find_one({ '_id': ObjectId(id) })   
    return render_template('showGeneralPartner.html', generalPartner = generalPartnerSet, t=title, h=heading)

#This is for update button
@app.route("/show", methods = ['GET'])
def viewGeneralPartner():
    id = request.values.get("_id")
    generalPartnerSet = generalPartners.find_one({ '_id':   ObjectId(id)})   
    return render_template('showGeneralPartner.html', generalPartner = generalPartnerSet, t=title, h=heading)


#This is for making rest call for query
@app.route("/restquery", methods = ['POST'])
def queryGeneralPartner():
    response = requests.get("http://localhost:5000/partner/Westfield%20Topanga+Westfield%20JV")
    generalPartnerSet = response.json() 
    return render_template('showGeneralPartner.html', generalPartner = generalPartnerSet, t=title, h=heading)

if __name__ == "__main__":
    #app.run(debug=True)
    #app.run(host='10.35.112.108', port=8080)
    app.run(host='0.0.0.0', port=8080, debug=True)
    
# Careful with the debug mode..

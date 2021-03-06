from flask import Flask, jsonify, render_template, redirect, request
import urllib.request
import os
import json
import decimal

URL = 'http://credit-cards.98he2uhpu4.us-east-2.elasticbeanstalk.com/CurrentCards/CurrentValue'
with urllib.request.urlopen(URL) as url:
    CurrentValue = json.loads(url.read().decode())
CurrentValue.sort(key=lambda x: x['Value'], reverse=True)

application = Flask(__name__)

title = "Credit Cards"
heading = "Credit Card Introduction Bonuses"


programs = sorted(set([CurrentValue[i]['Program'] for i in range((len(CurrentValue)-1))]))
issuers = sorted(set([CurrentValue[i]['Issuer'] for i in range((len(CurrentValue)-1))]))

type = 'All'
program = 'All'
issuer = 'All'
fee = 550
spend = 5000
fee_waived = 0

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

#List All Cards
@application.route("/")
@application.route("/list")
def list():
    with urllib.request.urlopen(URL) as url:
        CurrentValue = json.loads(url.read().decode())
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)
    return(render_template('index.html',cards=CurrentValue, programs=programs, issuers=issuers, t=title,
                           h=heading, type=type, program=program, issuer=issuer, spend=spend, fee=fee))

#Edit Card Info
@application.route("/view")
def view():
    with urllib.request.urlopen(URL) as url:
        CurrentValue = json.loads(url.read().decode())
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)
    return(render_template('view.html',cards=CurrentValue, t=title, h=heading))

# Individual Card Pages
@application.route('/card/<name>', methods=['GET'])
def cardname(name):
    with urllib.request.urlopen(URL) as url:
        CurrentValue = json.loads(url.read().decode())
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)
    card = [x for x in CurrentValue if x['CardName'] == name]
    return render_template("card.html", cards=card, t=title, h=heading)

# Filter Cards
@application.route("/filter", methods=['POST'])
def filter():
    fee_waived = 0
    type=request.values.get("type")
    program=request.values.get("programs")
    issuer=request.values.get("issuers")
    business=request.values.get("business")
    fee=int(request.values.get("fee"))
    fee_waived=request.values.get("fee_waived")
    spend=int(request.values.get("spend"))

    with urllib.request.urlopen(URL) as url:
        CurrentValue = json.loads(url.read().decode())
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)

    if(program!='All'):
        CurrentValue = [x for x in CurrentValue if x['Program'] == program]
    if(type!='All'):
        CurrentValue = [x for x in CurrentValue if x[type] > 0]
    if(issuer!='All'):
        CurrentValue = [x for x in CurrentValue if x['Issuer'] == issuer]
    if(business!='All'):
        CurrentValue = [x for x in CurrentValue if x['business'] == business]
    if(fee!=550):
        CurrentValue = [x for x in CurrentValue if int(x['Fee']) <= fee]
    if(fee_waived!=0):
        CurrentValue = [x for x in CurrentValue if (int(x['FeeWaived1stYr'])-1)*int(x['Fee']) >= 0]
    if(spend!=5000):
        CurrentValue = [x for x in CurrentValue if int(x['Spend']) <= spend]
    return(render_template('index.html',cards=CurrentValue,t=title,h=heading, programs=programs, issuers=issuers, type=type,
                           program=program, issuer=issuer, spend=spend, fee=fee))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()


    

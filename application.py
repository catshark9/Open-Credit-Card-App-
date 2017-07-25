from flask import Flask, jsonify, render_template, redirect, request
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal


TABLE_NAME = 'CurrentValues'
REGION = "us-east-2"
ACCESS_KEY = 'AKIAIBDUUPJK5BAHMYRQ'
SECRET_KEY = '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'

dynamodb = boto3.resource('dynamodb', region_name=REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

table = dynamodb.Table(TABLE_NAME)

CurrentValue = table.scan()
CurrentValue = CurrentValue['Items']
CurrentValue.sort(key=lambda x: x['Value'], reverse=True)

application = Flask(__name__)

title = "Credit Cards"
heading = "Credit Card Introduction Bonuses"


programs = sorted(set([table.get_item(Key={'Id':i})['Item']['Program'] for i in range((len(CurrentValue)-1))]))
issuers = sorted(set([table.get_item(Key={'Id':i})['Item']['Issuer'] for i in range((len(CurrentValue)-1))]))

type = 'All'
program = 'All'
issuer = 'All'

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

#List All Cards
@application.route("/")
@application.route("/list")
def list():
    CurrentValue = table.scan()
    CurrentValue = CurrentValue['Items']
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)
    return(render_template('index.html',cards=CurrentValue, programs=programs, issuers=issuers, t=title, h=heading, type=type, program=program, issuer=issuer))

#Edit Card Info
@application.route("/view")
def view():
    CurrentValue = table.scan()
    CurrentValue = CurrentValue['Items']
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)
    return(render_template('view.html',cards=CurrentValue, t=title, h=heading))

# Individual Card Pages
@application.route('/card/<name>', methods=['GET'])
def cardname(name):
    CurrentValue = table.scan()
    CurrentValue = CurrentValue['Items']
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)
    card = [x for x in CurrentValue if x['CardName'] == name]
    return render_template("card.html", cards=card, t=title, h=heading)

# Remove a Card
@application.route("/delete")
def delete():
    key=request.values.get("Id")
    table.delete_item(
        Key={'Id': int(key)}
    )
    return(redirect("/view"))

# Update A Card Page
@application.route("/update")
def update():
    key=int(request.values.get("Id"))
    CurrentValue = table.scan()
    CurrentValue = CurrentValue['Items']
    card = [x for x in CurrentValue if x['Id'] == key]
    return render_template('update.html',cards=card,h=heading,t=title)

@application.route("/modify_action", methods=['POST'])
def modify_action():
    #Updating a card with various references
    name=request.values.get("name")
    cash=request.values.get("cash")
    points=request.values.get("points")
    nights=request.values.get("nights")
    spend=request.values.get("spend")
    fee=request.values.get("fee")
    v=request.values.get("value")
    key=request.values.get("Id")

    table.update_item(
        Key={
            'Id': int(key)
        },
        UpdateExpression='SET CardName = :name, Cash = :cash, Points = :points, Nights = :nights, Spend = :spend, Fee = :fee',
        ExpressionAttributeValues={
            ':name': name,
            ':cash': decimal.Decimal(cash),
            ':points': decimal.Decimal(points),
            ':nights': decimal.Decimal(nights),
            ':spend': decimal.Decimal(spend),
            ':fee': decimal.Decimal(fee),
        }
    )
    return(redirect("/view"))

# Filter Cards
@application.route("/filter", methods=['POST'])
def filter():
    type=request.values.get("type")
    program=request.values.get("programs")
    issuer=request.values.get("issuers")
    business=request.values.get("business")

    CurrentValue = table.scan()
    CurrentValue = CurrentValue['Items']
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)

    if(program!='All'):
        CurrentValue = [x for x in CurrentValue if x['Program'] == program]
    if(type!='All'):
        CurrentValue = [x for x in CurrentValue if x[type] > 0]
    if(issuer!='All'):
        CurrentValue = [x for x in CurrentValue if x['Issuer'] == issuer]
    if(business!='All'):
        CurrentValue = [x for x in CurrentValue if x['business'] == business]
		
    return(render_template('index.html',cards=CurrentValue,t=title,h=heading, programs=programs, issuers=issuers, type=type, program=program, issuer=issuer))



@application.route("/CurrentCards/CurrentValue", methods=['GET'])
def CurrentCards_CurrentValue():
    CurrentValue = table.scan()
    CurrentValue = CurrentValue['Items']
    CurrentValue.sort(key=lambda x: x['Value'], reverse=True)

    return(CurrentValue)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()


    

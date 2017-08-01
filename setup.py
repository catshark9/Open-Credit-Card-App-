import csv
import json
import sys, getopt, pprint
import os.path
import re
import boto3


TABLE_NAME = 'CurrentValues'


dynamodb = boto3.resource('dynamodb', region_name=REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
table = dynamodb.Table(TABLE_NAME)

FIELDS = {'CardName': True, 'Program': True, 'Issuer': True, 'Link': True, 'Cash': True, 'Points': True, 'Nights': True, 'Credit': True, 'Fee': True, 'img': True, 'Spend': True, 'Rate': True, 'Value': True, '_id': False}


csvfile = open("C:/Users/Administrator/Documents/Applications/CreditCard/data/CurrentValues.csv")
reader = csv.DictReader( csvfile )

header= ["CardName", "Program", "Issuer",	 "Link",	"IntroOffer",	"Cash",	"Points",	"Nights",	"Credit",	"FeeWaived1stYr", "Fee", "Spend",	"img",	"Rate",	 "Value", "business"]
i = 0
for each in reader:
    row={}
    row['Id'] = i
    for field in header:
        if field in ['Value', 'Cash', 'Points', 'Nights']:
            each[field] = re.sub("\.00E\+05", "00000", each[field])
            row[field]=int(each[field])
        else:
            row[field]=each[field]
    table.put_item(Item=row)
    i = i + 1

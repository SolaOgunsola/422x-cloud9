from app import app
from flask import render_template, request, redirect, url_for
import boto3
from boto3.dynamodb.conditions import Key
from os import environ

S3_SECRET = environ.get('S3_SECRET')
S3_KEY = environ.get('S3_KEY')

@app.route('/AddICar', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        make = request.form['make']
        manu = request.form['manu']
        descrip = request.form['descrip']
        price = request.form['price']
        color = request.form['color']
        miles = request.form['miles']
        year = request.form['year']
        condition = request.form['condition']
        phone = request.form['phone']
        city = request.form['city']

        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('ForSale')
        dTable = {
            "category": "car",
            "City": city,
            "Color": color,
            "Condition": condition,
            "Manufacturer": manu,
            "Make": make,
            "Miles": miles,
            "PhoneNumber": phone,
            "Description": descrip,
            "Price": price,
            "Year": year,
        }
        table.put_item(Item=dTable)

    return render_template("public/index.html")


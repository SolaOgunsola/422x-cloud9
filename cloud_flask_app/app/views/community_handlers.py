from app import app
from flask import render_template, request, redirect, Response
from werkzeug.utils import secure_filename
import boto3
from boto3.dynamodb.conditions import Key
from os import environ
import time

# UPLOAD_FOLDER = "uploads"
BUCKET = str(environ.get('S3_BUCKET'))
S3_SECRET = environ.get('S3_SECRET')
S3_KEY = environ.get('S3_KEY')
contents = None

@app.route('/user/AddCommunity', methods=['GET', 'POST'])
def addCommunity():
    print("Request Method: " + request.method)
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Community')
        dTable = {
            "itemCode": time.time_ns(),
            "category": request.form['category'],
            "description": request.form['description'],
            "location": request.form['location'],
            "time": request.form['time'],
            "requirements": request.form['requirements'],
            "PhoneNumber": request.form['phone']
        }
        print(dTable)
        table.put_item(Item=dTable)
        return redirect("/")

    return render_template("user/AddCommunity.html")

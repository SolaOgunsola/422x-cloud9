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

@app.route('/user/AddHousing', methods=['GET', 'POST'])
def addHousing():
    print("Request Method: " + request.method)
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Housing')
        dTable = {
            "itemCode": time.time_ns(),
            "category": request.form['category'],
            "location": request.form['location'],
            "size": request.form['size'],
            "rent": request.form['rent'],
            "description": request.form['description'],
            "PhoneNumber": request.form['phone']
        }
        print(dTable)
        table.put_item(Item=dTable)
        return redirect("/")

    return render_template("user/AddHousing.html")
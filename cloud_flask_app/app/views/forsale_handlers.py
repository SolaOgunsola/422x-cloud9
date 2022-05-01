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

@app.route('/user/AddForSale/<category>', methods=['GET', 'POST'])
def addForSale(category):
    # Post Handling
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET, region_name="us-east-1")
        table = dynamodb.Table('ForSale')
        dTable = formatJson(request.form)
        table.put_item(Item=dTable)
        return redirect("/")

    # Get Handling
    if category == 'art':
        return render_template("user/AddForSale/AddArt.html")
    elif category == 'boat':
        return render_template("user/AddForSale/AddBoat.html")
    elif category == 'car':
        return render_template("user/AddForSale/AddCar.html")
    elif category == 'furniture':
        return render_template("user/AddForSale/AddFurniture.html")
    elif category == 'tv':
        return render_template("user/AddForSale/AddTV.html")
    else:
        print('No category input. Redirecting to home.')
        return redirect("/")


def formatJson(form):
    newDictionary = {}
    keys = form.keys()
    newDictionary["itemCode"] = time.time_ns()
    for key in keys:
        newDictionary[key] = form[key]
    # Debug
    print(newDictionary)
    return newDictionary


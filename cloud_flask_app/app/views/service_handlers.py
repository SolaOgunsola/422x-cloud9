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

@app.route('/user/AddServices/<category>', methods=['GET', 'POST'])
def addService(category):
    # Post Handling
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET, region_name="us-east-1")
        table = dynamodb.Table('Jobs')
        dTable = formatJson(request.form)
        table.put_item(Item=dTable)
        return redirect("/")

    # Get Handling
    if category == 'automotive':
        return render_template("user/AddService/AddAutomotive.html")
    elif category == 'computer':
        return render_template("user/AddService/AddComputer.html")
    elif category == 'legal':
        return render_template("user/AddService/AddLegal.html")
    elif category == 'lesson':
        return render_template("user/AddService/AddLesson.html")
    elif category == 'pet':
        return render_template("user/AddService/AddPet.html")
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

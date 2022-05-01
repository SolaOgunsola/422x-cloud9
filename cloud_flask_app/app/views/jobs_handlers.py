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

@app.route('/user/AddJob/<category>', methods=['GET', 'POST'])
def addJob(category):
    # Post Handling
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET, region_name="us-east-1")
        table = dynamodb.Table('Jobs')
        dTable = formatJson(request.form)
        table.put_item(Item=dTable)
        return redirect("/")

    # Get Handling
    if category == 'education':
        return render_template("user/AddJob/AddEducation.html")
    elif category == 'finance':
        return render_template("user/AddJob/AddFinance.html")
    elif category == 'food':
        return render_template("user/AddJob/AddFood.html")
    elif category == 'legal':
        return render_template("user/AddJob/AddLegal.html")
    elif category == 'software':
        return render_template("user/AddJob/AddSoftware.html")
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


def addJob():
    print("Request Method: " + request.method)
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Jobs')
        dTable = {
            "itemCode": time.time_ns(),
            "category": request.form['category'],
            "experience": request.form['experience'],
            "salary": request.form['salary'],
            "location": request.form['location'],
            "description": request.form['description'],
            "PhoneNumber": request.form['phone']
        }
        print(dTable)
        table.put_item(Item=dTable)
        return redirect("/")

    return render_template("user/AddJob.html")

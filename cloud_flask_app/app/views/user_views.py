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

@app.route("/guestLogin")
def guest_login():
    environ.update(LOGIN='0')
    return redirect("/")


@app.route('/ForSale/<category>', methods=['GET', 'POST'])
def get_forsale_items(category):
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
    table = dynamodb.Table('ForSale')
    response =table.scan()
    contents = []
    for i in response['Items']:
        if category == (i['category'].lower()):
            print(i)
            contents.append(i)
    return render_template('user/ListViewForSale.html', title=category,loggedIn=environ.get('LOGIN'), contents=contents)


@app.route('/Community/<category>', methods=['GET', 'POST'])
def get_community_items(category):
    # Categories: events, lost and found, classes, volunteering, rideshare
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
    table = dynamodb.Table('Community')
    response =table.scan()
    contents = []
    for i in response['Items']:
        i['category'] = i['category'].lower()
        if category == (i['category'].lower()):
            print(i)
            contents.append(i)
    print('title: ' + category, 'loggedIn: ' + environ.get('LOGIN') + '!!!!!!!!!!')
    return render_template('user/ListViewCommunity.html',title=category, loggedIn=environ.get('LOGIN'), url="/user/AddCommunity/" + category, contents=contents)

@app.route('/Housing/<category>', methods=['GET', 'POST'])
def get_housing_items(category):
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
    table = dynamodb.Table('Housing')
    response =table.scan()
    contents = []
    for i in response['Items']:
        if category == (i['category']):
            print(i)
            contents.append(i)
    return render_template('user/ListViewHousing.html',title=category, loggedIn=environ.get('LOGIN'),contents=contents)

@app.route('/Jobs/<category>', methods=['GET', 'POST'])
def get_jobs_items(category):
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
    table = dynamodb.Table('Jobs')
    response =table.scan()
    contents = []
    for i in response['Items']:
        if category == (i['category']):
            print(i)
            contents.append(i)
    return render_template('user/ListViewJob.html',title=category, loggedIn=environ.get('LOGIN'),contents=contents)

@app.route('/Services/<category>', methods=['GET', 'POST'])
def get_services_items(category):
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
    table = dynamodb.Table('Services')
    response =table.scan()
    contents = []
    for i in response['Items']:
        if category == (i['category']):
            print(i)
            contents.append(i)
    return render_template('user/ListViewServices.html',title=category,loggedIn=environ.get('LOGIN'), contents=contents)


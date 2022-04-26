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

@app.route("/")
def user_dashboard():
    return render_template("public/index.html")

@app.route('/ForSale/<category>', methods=['GET', 'POST'])
def get_forsale_items(category):
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
    table = dynamodb.Table('ForSale')
    response =table.scan()
    contents = []
    for i in response['Items']:
        if category == (i['category']):
            print(i)
            contents.append(i)
    return render_template('user/ListViewForSale.html', title=category,loggedIn=environ.get('LOGIN'), contents=contents)


@app.route('/Community/<category>', methods=['GET', 'POST'])
def get_community_items(category):
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
    table = dynamodb.Table('Community')
    response =table.scan()
    contents = []
    for i in response['Items']:
        if category == (i['category']):
            print(i)
            contents.append(i)
    print('title: ' + category, 'loggedIn: ' + environ.get('LOGIN') + '!!!!!!!!!!')
    return render_template('user/ListViewCommunity.html',title=category, loggedIn=environ.get('LOGIN'), contents=contents)

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


@app.route('/user/AddForSale', methods=['GET', 'POST'])
def addForSale():
    print("Request Method: " + request.method)
    if request.method == 'POST':
        make = request.form['make']
        category = request.form['category']
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
            "itemCode": time.time_ns(),
            "category": category,
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
        print(dTable)
        table.put_item(Item=dTable)
        return redirect("/user/dashboard")

    return render_template("user/AddForSale.html")

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
        return redirect("/user/dashboard")

    return render_template("user/AddCommunity.html")

@app.route('/user/AddHousing', methods=['GET', 'POST'])
def addHousing():
    print("Request Method: " + request.method)
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Community')
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
        return redirect("/user/dashboard")

    return render_template("user/AddHousing.html")

@app.route('/user/AddJob', methods=['GET', 'POST'])
def addJob():
    print("Request Method: " + request.method)
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Community')
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
        return redirect("/user/dashboard")

    return render_template("user/AddJob.html")

@app.route('/user/AddService', methods=['GET', 'POST'])
def addService():
    print("Request Method: " + request.method)
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Community')
        dTable = {
            "itemCode": time.time_ns(),
            "category": request.form['category'],
            "availability": request.form['availability'],
            "location": request.form['location'],
            "description": request.form['description'],
            "price": request.form['price'],
            "PhoneNumber": request.form['phone']
        }
        print(dTable)
        table.put_item(Item=dTable)
        return redirect("/user/dashboard")

    return render_template("user/AddService.html")

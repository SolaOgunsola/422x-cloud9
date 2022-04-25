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

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        resource = boto3.resource('s3')
        bucket = resource.Bucket(BUCKET)
        bucket.Object(f.filename).put(Body=f)
        # add to dynamodb
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Images')
        ImageObj = {
            "ImageName": f.filename,
            "UserName": environ.get('USERNAME')
        }
        table.put_item(Item=ImageObj)
    return redirect("/user/dashboard")

@app.route("/download", methods=['POST'])
def download():
    obj_key = request.form['key']
    resource = boto3.resource('s3')
    bucket = resource.Bucket(BUCKET)
    file_obj = bucket.Object(obj_key).get()

    resp = Response(file_obj['Body'].read())
    resp.headers['Content-Disposition'] = 'attachment;filename=' + format(obj_key)
    resp.mimetype = 'text/plain'

    return resp


@app.route('/ForSale/<category>', methods=['GET', 'POST'])
def get_items(category):
    dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
    table = dynamodb.Table('ForSale')
    response =table.scan()
    contents = []
    for i in response['Items']:
        if category == (i['category']):
            print(i)
            contents.append(i)
    return render_template('user/ListViewForSale.html', contents=contents)

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
            "description": request.form['description'],
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

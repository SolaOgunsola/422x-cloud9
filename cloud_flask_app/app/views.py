from app import app
from flask import render_template, request, redirect, url_for
import boto3
from boto3.dynamodb.conditions import Key
from os import environ

S3_SECRET = environ.get('S3_SECRET')
S3_KEY = environ.get('S3_KEY')

# TODO update? since login has mo
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Users')
        response =table.query(KeyConditionExpression=Key('username').eq(str(username)))
        for i in response['Items']:
            print(i)
            checkPword = (i['password'])
            if checkPword == password:
                #redirect to new page
                environ.update(USERNAME=username)
                environ.update(LOGIN='1')
                print(environ.get('USERNAME'))
                return redirect("user/dashboard")    
    return render_template("public/index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # conn = 
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=S3_KEY,aws_secret_access_key=S3_SECRET,region_name="us-east-1")
        table = dynamodb.Table('Users')
        dynamoCanBlowMe = {
            "username": username,
            "password": password
        }
        table.put_item(Item=dynamoCanBlowMe)
        return render_template("user/login.html")

    return render_template("public/register.html")

import os
import boto3
from app import app
from flask import render_template, request, redirect, Response
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = "uploads"
BUCKET = "photos422"


@app.route("/user/dashboard")
def user_dashboard():
    # show_image retrieves a list of temporary, public image urls
    # contents = show_image(BUCKET)
    contents = get_bucket_files(BUCKET)
    # contents is passed to the dashboard.html file
    return render_template("user/dashboard.html", contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        resource = boto3.resource('s3')
        bucket = resource.Bucket('photos422')
        bucket.Object(f.filename).put(Body=f)
    
    return redirect("/user/dashboard")

@app.route("/download", methods=['POST'])
def download():
    obj_key = request.form['key']
    resource = boto3.resource('s3')
    bucket = resource.Bucket('photos422')
    file_obj = bucket.Object(obj_key).get()

    resp = Response(file_obj['Body'].read())
    resp.headers['Content-Disposition'] = 'attachment;filename=' + format(obj_key)
    resp.mimetype = 'text/plain'

    return resp

@app.route('/search', methods=['GET'])
def search():
    file_name = request.args.get("search")
    resource = boto3.resource('s3')
    bucket = resource.Bucket('photos422')
    object_list = bucket.objects.filter(Prefix=file_name)

    return render_template('user/dashboard.html', contents=object_list)

def show_image(bucket):
    s3_client = boto3.client('s3')
    # public_urls = []
    files = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            # presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
            # tuple = (presigned_url, item['Key'])
            # public_urls.append(tuple)
            # print(tuple)
            files.append(item['Key'])

    except Exception as e:
        print(e)
        pass
    return files

def upload_file(file_name, bucket):
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

def get_bucket_files(bucket):
    resource = boto3.resource('s3')
    bucket = resource.Bucket('photos422')
    object_list = bucket.objects.all()

    return object_list

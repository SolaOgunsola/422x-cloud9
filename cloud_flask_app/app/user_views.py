import os
import boto3
from app import app
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
BUCKET = "photos422"


@app.route("/user/dashboard")
def user_dashboard():
    # show_image retrieves a list of temporary, public image urls
    contents = show_image(BUCKET)
    # contents is passed to the dashboard.html file
    return render_template("user/dashboard.html", contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"uploads/{f.filename}", BUCKET)
        return redirect("/user/dashboard")

def show_image(bucket):
    s3_client = boto3.client('s3')
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
            public_urls.append(presigned_url)
            print("URL: " + presigned_url)

    except Exception as e:
        pass
    return public_urls

def upload_file(file_name, bucket):
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

from app import app
from flask import render_template, request, redirect, url_for
import pymysql

@app.route('/', methods=['GET', 'POST'])
def index():
    print("here")	
    conn = pymysql.connect(
            host= 'database-1.czglra39ojmn.us-east-1.rds.amazonaws.com', 
            port = 3306,
            user = 'admin', 
            password = 'password',
            db = 'db',
            )
    with conn:
            with conn.cursor() as cursor:
                print("conn")
                if request.method == 'POST':
                    username = request.form['username']
                    password = request.form['password']
                    cur=conn.cursor()
                    query = "SELECT password from users Where username = '" + str(username) + "'"
                    print(query)
                    cur.execute(query)
                    output = cur.fetchall()
                    if password == output[0][0]:
                        print("check made")
                        return redirect("/user/dashboard")    
    
    return render_template("public/index.html")

# @app.route("/about")
# def about():
#     return render_template("public/index.html")

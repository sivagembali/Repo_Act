import sqlite3
import json
import hackerrank_and_github_response
from flask import Flask, redirect, url_for, request,current_app
app = Flask(__name__)

@app.route('/')
def root():
    return current_app.send_static_file('login.html')

@app.route('/login',methods = ['POST'])
def login():
    conn = sqlite3.connect('userdatabase.db')
    emailnumber = request.form['emailormobile']
    pswd = request.form['password']
    details = (pswd,emailnumber,emailnumber)
    cursor = conn.execute("SELECT PASSWORD,EMAIL,MOBILE FROM STUDENTREGISTRATION WHERE PASSWORD= ? AND (EMAIL = ? OR MOBILE= ?) ",details)
    data = cursor.fetchall()
    conn.close()
    #print(len(data))
    if(len(data)):
        return "Successfully loggedin"
    else:
        return "Invalid Credentials"


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

#This module is to store data from the registration form.
@app.route('/register',methods = ['POST'])
def register():
    database_connection = sqlite3.connect('userdatabase.db')
    username = request.form['name']
    password = request.form['password']
    collegename = request.form['collegename']
    email = request.form['email']
    mobile = request.form['mobile']
    user_details = (username,password,email,mobile,collegename)
    insertion_query = '''INSERT INTO STUDENTREGISTRATION(NAME,PASSWORD,EMAIL,MOBILE,COLLEGENAME) VALUES(?,?,?,?,?)'''
    database_connection.execute(insertion_query,user_details)
    database_connection.commit()
    database_connection.close()
    return "Successfully registred"
    

    
@app.route('/updateuserperformance/<userid>')
def update_user_performance(userid):
    result = hackerrank_and_github_response.update_user_performance_data(userid)
    #print(result)
    json_string = json.dumps(result)
    return json_string
    

if __name__ == '__main__':
   app.run(debug=True)
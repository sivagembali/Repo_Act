import sqlite3
import json
import hackerrank_and_github_response
from flask import Flask, redirect, url_for, request,current_app
app = Flask(__name__)

#@app.route('/')
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
    cursor.close()
    conn.close()
    #print(len(data))
    if(len(data)):
        return "Successfully Loggedin"
    else:
        return "Invalid Credentials"
#redirect("/static/updation_page.html")

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
    if(username =='' or password =='' or collegename=='' or email=='' or mobile==''):
        return "All Fields are Mandatory"
    else:
        email_validation = hackerrank_and_github_response.check_mail(email)
        if(len(email_validation)):
            database_connection.close()
            return "Email already exist"
        else:
            user_details = (username,password,email,mobile,collegename)
            insertion_query = '''INSERT INTO STUDENTREGISTRATION(NAME,PASSWORD,EMAIL,MOBILE,COLLEGENAME) VALUES(?,?,?,?,?)'''
            database_connection.execute(insertion_query,user_details)
            database_connection.commit()
            student_info = hackerrank_and_github_response.check_mail(email)
            #print(student_info['studentinfo'])
            value = student_info['userid']
            database_connection.execute("INSERT INTO STUDENTPERFORMANCE(USERID) VALUES (%s)"% value)
            database_connection.commit()
            database_connection.close()
            return "Successfully Registred"

    
@app.route('/updateuserperformance/<userid>')
def update_user_performance(userid):
    result = hackerrank_and_github_response.update_user_performance_data(userid)
    json_string = json.dumps(result)
    return json_string

@app.route('/updateall')
def update_all_status():
    result = hackerrank_and_github_response.update_all_users_status()
    return result
    
@app.route('/update_ids',methods = ['POST'])
def update_ids():
    email = request.form['email']
    hackerrankid=request.form['hackerrankid']
    githubid=request.form['githubid']
    if(hackerrankid=='' or githubid==''):
        return "All Fields are Mandatory"
    else:
        ids = {}
        ids['email_id']=email
        ids['hackerrank_id']=hackerrankid
        ids['github_id']=githubid
        result = hackerrank_and_github_response.update_all_ids(ids)
        #to update all students status
        #hackerrank_and_github_response.update_all_users_status()
        return result

@app.route('/dashboard')
def dashboard():
    mail = request.args.get('email')
    user_id = hackerrank_and_github_response.get_id_for_email(mail)
    #print("In side dashboard--",user_id)
    result = hackerrank_and_github_response.get_status_data(user_id)
    #print("In side Dashboard result--",result)
    return result

if __name__ == '__main__':
   app.run(debug=True)
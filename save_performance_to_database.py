import sqlite3

#Method to save students hackerrank and github status
def save_u_p_data(hackerrank_github_data):
    database_connection = sqlite3.connect('userdatabase.db')
    user_id = hackerrank_github_data['userid']
    hackerrank_info = hackerrank_github_data['hackerrank_data']
    github_info = hackerrank_github_data['github_data']
    database_connection.execute("UPDATE STUDENTPERFORMANCE SET HACKERRANK_STATUS=?,GITHUB_STATUS=? WHERE USERID = ?",(hackerrank_info,github_info,user_id))
    database_connection.commit()
    database_connection.close()
    #print("Successfully Updated")

#Method to create tables STUDENTPERFORMANCE STUDENTREGISTRATION
def creation_tables():
    database_connection = sqlite3.connect('userdatabase.db')
    database_connection.execute('''CREATE TABLE STUDENTREGISTRATION (USERID INTEGER PRIMARY KEY,NAME TEXT NOT NULL,PASSWORD TEXT NOT NULL,EMAIL TEXT UNIQUE,MOBILE TEXT NOT NULL,COLLEGENAME TEXT NOT NULL);''')
    database_connection.execute('''CREATE TABLE STUDENTPERFORMANCE(S_NUMBER INTEGER PRIMARY KEY ,HACKERRANKID TEXT,GITHUBID TEXT,HACKERRANK_STATUS TEXT,GITHUB_STATUS TEXT,LINKEDINID TEXT,STACKOVERFLOWID TEXT,USERID INTEGER,FOREIGN KEY (USERID) REFERENCES STUDENTREGISTRATION(USERID) )''')
    database_connection.close()
    
#Method to insert data into tables
def insert_data():
    database_connection = sqlite3.connect('userdatabase.db')
    database_connection.execute("INSERT INTO STUDENTREGISTRATION (USERID,NAME,PASSWORD,EMAIL,MOBILE,COLLEGENAME) VALUES(1,'siva gembali','sanjana','ssiva356@gmail.com','8978098160','GVP College');")
    database_connection.execute("INSERT INTO STUDENTPERFORMANCE (S_NUMBER,HACKERRANKID,GITHUBID,USERID) VALUES(1,'sivagembali','sivagembali',1);")
    database_connection.commit()
    database_connection.close()
    
#creation_tables()
#insert_data()

#Method to retrive data from database returns a json 
def get_ids_studentperformance(userid):
    database_connection = sqlite3.connect('userdatabase.db')
    data_cursor = database_connection.cursor()
    result_cursor = data_cursor.execute("SELECT HACKERRANKID,GITHUBID FROM STUDENTPERFORMANCE WHERE USERID = %s "% userid)
    result_data_set={}
    result_data_set['userid']=userid
    result_data = result_cursor.fetchall()
    for row in result_data:
        result_data_set['hackerrankid']=row[0]
        result_data_set['githubid']=row[1]
    data_cursor.close()
    database_connection.close()
    return result_data_set

#Method to retrive s_numbers from student performance table returns all students s_nubers 
def get_snumber_from_studentperformance_table():
    database_connection = sqlite3.connect('userdatabase.db')
    data_cursor = database_connection.cursor()
    data_cursor = database_connection.execute("SELECT USERID FROM STUDENTPERFORMANCE")
    resultant_data = data_cursor.fetchall()
    data_cursor.close()
    database_connection.close()
    return resultant_data

#Method to check email exist in the database or not if exist returns student info(foreign key value) of type dictionary
def check_email_exist_or_not(email):
    database_connection = sqlite3.connect('userdatabase.db')
    data_cursor = database_connection.cursor()
    data_cursor = database_connection.execute("SELECT USERID FROM STUDENTREGISTRATION WHERE EMAIL='%s'" % email)
    resultant_data = data_cursor.fetchall()
    result = {}
    for row in resultant_data:
        result['userid']=row[0]
    data_cursor.close()
    database_connection.close()
    return result
#print(check_email_exist_or_not('ssiva356@gmail.com'))

#Method to update hackerrankid and githubid and returns status  message
def update_ids_to_database(user_details):
    database_connection = sqlite3.connect('userdatabase.db')
    student_info = user_details['userid']
    hackerrank_id = user_details['hackerrankid']
    github_id=user_details['github_id']
    #print(hackerrank_id,github_id,student_info)
    database_connection.execute("UPDATE STUDENTPERFORMANCE SET HACKERRANKID = ?,GITHUBID = ? WHERE USERID = ?",(hackerrank_id,github_id,student_info))
    #database_connection.execute("INSERT INTO STUDENTPERFORMANCE(HACKERRANKID,GITHUBID,STUDENTINFO) VALUES(?,?,?)",(hackerrank_id,github_id,student_info))
    #print("changes",database_connection.total_changes)
    database_connection.commit()
    database_connection.close()
    return "Successfully Updated"

#Method to retrive data from database returns a json with github and hackerrank status
def get_student_github_hackerrank_status(student_info):
    database_connection = sqlite3.connect('userdatabase.db')
    data_cursor = database_connection.cursor()
    data_cursor = database_connection.execute("SELECT HACKERRANK_STATUS,GITHUB_STATUS FROM STUDENTPERFORMANCE WHERE USERID='%s'" % student_info)
    data = data_cursor.fetchall()
    result_status = {}
    for row in data:
        result_status['hackerrank_status']=row[0]
        result_status['github_status']=row[1]
    return result_status
    
    
def get_all_students_data():
    database_connection = sqlite3.connect('userdatabase.db')
    data_cursor = database_connection.cursor()
    data_cursor = database_connection.execute("SELECT * FROM STUDENTREGISTRATION")
    data = data_cursor.fetchall()
    result_status = {}
    for row in data:
        s_id = row[0]
        result_status[s_id] = {}
        result_status[s_id]['name:']=row[1]
        result_status[s_id]['password']=row[2]
        result_status[s_id]['email'] = row[3]
        result_status[s_id]['mobile'] = row[4]
        result_status[s_id]['college']= row[5]
    return result_status
    #print(result_status)
#get_all_students_data()

    
    
"""#Method to store the data coming from the user registration
def save_user_registration_data(user_details):
    database_connection = sqlite3.connect('userdatabase.db')
    username = user_details['username']
    password = user_details['password']
    collegename = user_details['collegename']
    email = user_details['email']
    mobile = user_details['mobile']
    user_data = (username,password,email,mobile,collegename)
    insertion_query = '''INSERT INTO STUDENTREGISTRATION(NAME,PASSWORD,EMAIL,MOBILE,COLLEGENAME) VALUES(?,?,?,?,?)'''
    database_connection.execute(insertion_query,user_data)
    database_connection.commit()
    database_connection.close()
#save_user_registration_data({'username':'siva','password':'sanjuamma','email':'ssilva356@gmail.com','mobile':'8978098722','collegename':'gvp'})
"""


#creation_tables();
#insert_data();
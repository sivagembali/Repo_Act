import sqlite3

#Method to save students hackerrank and github status
def save_u_p_data(hackerrank_github_data):
    database_connection = sqlite3.connect('userdatabase.db')
    user_id = hackerrank_github_data['userid']
    hackerrank_info = hackerrank_github_data['hackerrank_data']
    github_info = hackerrank_github_data['github_data']
    database_connection.execute("UPDATE STUDENTPERFORMANCE SET HACKERRANK_STATUS=?,GITHUB_STATUS=? WHERE STUDENTINFO = ?",(hackerrank_info,github_info,user_id))
    database_connection.commit()
    database_connection.close()
    #print("Successfully Updated")

#Method to create tables STUDENTPERFORMANCE STUDENTREGISTRATION
def creation_tables():
    database_connection = sqlite3.connect('userdatabase.db')
    database_connection.execute('''CREATE TABLE STUDENTREGISTRATION (USERID INTEGER PRIMARY KEY,NAME TEXT NOT NULL,PASSWORD TEXT NOT NULL,EMAIL TEXT UNIQUE,MOBILE TEXT NOT NULL,COLLEGENAME TEXT NOT NULL);''')
    database_connection.execute('''CREATE TABLE STUDENTPERFORMANCE(S_NUMBER INTEGER PRIMARY KEY ,HACKERRANKID TEXT,GITHUBID TEXT,HACKERRANK_STATUS TEXT,GITHUB_STATUS TEXT,LINKEDINID TEXT,STACKOVERFLOWID TEXT,STUDENTINFO INTEGER,FOREIGN KEY (STUDENTINFO) REFERENCES STUDENTREGISTRATION(USERID) )''')
    database_connection.close()
    
#Method to insert data into tables
def insert_data():
    database_connection = sqlite3.connect('userdatabase.db')
    database_connection.execute("INSERT INTO STUDENTREGISTRATION (USERID,NAME,PASSWORD,EMAIL,MOBILE,COLLEGENAME) VALUES(1,'siva gembali','sanjana','ssiva356@gmail.com','8978098160','GVP College');")
    database_connection.execute("INSERT INTO STUDENTPERFORMANCE (S_NUMBER,HACKERRANKID,GITHUBID,STUDENTINFO) VALUES(1,'sivagembali','sivagembali',1);")
    database_connection.commit()
    database_connection.close()

#Method to retrive data from database
def get_ids_studentperformance(userid):
    database_connection = sqlite3.connect('userdatabase.db')
    data_cursor = database_connection.cursor()
    result_cursor = data_cursor.execute("SELECT HACKERRANKID,GITHUBID FROM STUDENTPERFORMANCE WHERE STUDENTINFO = %s "% userid)
    result_data_set={}
    result_data_set['userid']=userid
    result_data = result_cursor.fetchall()
    for row in result_data:
        result_data_set['hackerrankid']=row[0]
        result_data_set['githubid']=row[1]
    data_cursor.close()
    database_connection.close()
    return result_data_set


#creation_tables();
#insert_data();
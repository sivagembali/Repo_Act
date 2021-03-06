import save_performance_to_database
import json
import requests

#Method to get data from url link with hackerrank_id and return a json string
def get_hackerrank_data(hackerrank_id):
    #getting data from hackerrank url which returns a byte type data
    try:
        hackerrank_response_type_byte = requests.get("https://www.hackerrank.com/rest/hackers/%s/submission_histories" %hackerrank_id)
        hackerrank_data_type_dict = json.loads(hackerrank_response_type_byte.content)
        hackerrank_data_type_json_string = json.dumps(hackerrank_data_type_dict)
        return hackerrank_data_type_json_string
    except Exception as exc:
        return "No Data Available"

    
def hackerrank_url_call(hackerrank_id,cursor=''):
    try:
        data = requests.get("https://www.hackerrank.com/rest/hackers/%s/recent_challenges?limit=20&response_version=v2&cursor=%s"%(hackerrank_id, cursor))
        return json.loads(data.content)
    except Exception as exc:
        return 0
#print(hackerrank_url_call('sivagembali','MTA1NTQ2N3x8MTUxMTI4Njc2My4wfHwxXzEzNTAy'))
    
#Method to get data from url link with hackerrank id and returns number of problems solved with problem statements
def get_hackerrank_problems(hackerrank_id):
    try:
        result = {}
        cursor=''
        last_page = False
        list_of_problems=[]
        status = True
        st_for_question = True
        result_from_data_base = save_performance_to_database.get_hackerrank_problems_and_latest_qtn(hackerrank_id)
        data_from_database= json.loads(result_from_data_base)
        qtn_from_database = data_from_database['recent_problem']
        problems_list = data_from_database['problems_list']
        while(last_page!=True):
            data = hackerrank_url_call(hackerrank_id,cursor)
            if(st_for_question == True):
                st_for_question = False
                result['recent_problem']= data['models'][0]['name']
            #print(len(data['models']))
            for item in data['models']:
                if(item['name']!= qtn_from_database):
                    problems_list.append(item['name'])
                else:
                    status = False
                    break
            last_page= data['last_page']
            cursor= data['cursor']
            if(status == False):
                break
        #print("List of problems",problems_list)
        result['problems_list'] = problems_list
        result['problems_count'] = len(problems_list)
        #print(result)
        return json.dumps(result)
    except Exception as exc:
        #print("Exception",exc)
        return json.dumps({'problems_list':[],'problems_count':0,'recent_problem':''})
#print(get_hackerrank_problems('udayasriap'))


#method to get hackerrank data from database
def get_hackerrank_data_from_database(hackerrank_id):
    result = save_performance_to_database.get_hack_data_from_db(hackerrank_id)
    return result['hackerrank_status']
#get_hackerrank_data_from_database('sivagembali')
    

#method currently not working uncomment the url call
#print(get_hackerrank_data("kittusairam"))
#method to get data from url link with github_id and returns a json string
def get_github_data(github_id):
    #getting data from github using url and github_id
    #print(github_id)
    try:
        github_data = {}
        github_response_type_byte = requests.get("https://api.github.com/users/%s/repos"%github_id)
        github_response_data = json.loads(github_response_type_byte.content)
        #print(github_response_data)
        for repository_data in range(len(github_response_data)):
            repo_id = github_response_data[repository_data]['id']
            repo_data = {}
            repo_data['name'] = github_response_data[repository_data]['name']
            repo_data['created_at']= github_response_data[repository_data]['created_at']
            repo_data['pushed_at'] = github_response_data[repository_data]['pushed_at']
            github_data[repo_id]= repo_data
        repo_count = len(list(github_data.keys()))
        total_github_data = {'git_data':github_data,'repo_count':repo_count}
        github_data_type_json_string = json.dumps(total_github_data)
        #print(repo_count)
        #print("git dataa:",github_data_type_json_string)
        return github_data_type_json_string
    except Exception as exc:
        return json.dumps({'git_data':"No Data Available",'repo_count':0,'problem':'Error in getting data'})
#print(get_github_data('rajeunoia'))

#Method to get hackerrank and github data    
def get_data(user_id,hackerrank_id,github_id):
    hackerrank_and_github_data = {}
    hackerrank_and_github_data ['hackerrank_problems'] = get_hackerrank_problems(hackerrank_id)
    hackerrank_and_github_data ['userid']= user_id
    hackerrank_and_github_data ['hackerrank_data'] = get_hackerrank_data(hackerrank_id)
    hackerrank_and_github_data ['github_data'] = get_github_data(github_id)
    try:
        sum_data = 0
        dict_data =json.loads(hackerrank_and_github_data ['hackerrank_data'])
        if(type(dict_data) is dict):
            for key in dict_data.keys():
                sum_data = sum_data + int(dict_data[key])
            #print(type(int(dict_data['2016-07-22'])))
            hackerrank_and_github_data ['hackerrank_submissions']= sum_data
    except Exception as exc:
        hackerrank_and_github_data ['hackerrank_submissions']= 0
    return hackerrank_and_github_data
    
#print(get_data(1,'sivagembali','sivagembali'))
#result = get_data(1,'sivagembali','sivagembali')
#update_performance.update_hackerrank_github_data(result)

def update_user_performance_data(userid):
    user_details = save_performance_to_database.get_ids_studentperformance(userid)
    user_id = user_details['userid']
    hackerrank_id = user_details['hackerrankid']
    github_id = user_details['githubid']
    data = get_data(user_id,hackerrank_id,github_id)
    save_performance_to_database.save_u_p_data(data)
    return "Successfuly updated"
#update_user_performance_data(2)

#Method to update all users status retuns success message
def update_all_users_status():
    snumbers = save_performance_to_database.get_snumber_from_studentperformance_table()
    for data in snumbers:
        update_user_performance_data(data[0])
    return "Successfuly updated"

#Method to update all ids and retutns message status
def update_all_ids(ids):
    email = ids['email_id']
    #print("inside update_all_ids--",ids)
    student_info_dict = save_performance_to_database.check_email_exist_or_not(email)
    if(len(student_info_dict)):
        user_details={}
        user_details['userid'] =  student_info_dict['userid']
        user_details['hackerrankid'] = ids['hackerrank_id']
        user_details['github_id'] = ids['github_id']
        status = save_performance_to_database.update_ids_to_database(user_details)
        return status
    else:
        return "Email not registred"

#Method return studentinfo to get hackerrank status and github status
def check_mail(email):
    result = save_performance_to_database.check_email_exist_or_not(email)
    return result
#print(check_mail('ssiva356@gmail.com'))
#{'studentinfo':1}
#Method to get status data from datbase and returns json string
def get_status_data(userid):
    result_from_database = save_performance_to_database.get_student_github_hackerrank_status(userid)
    json_string = json.dumps(result_from_database)
    return json_string

#modified on 25th feb 
def get_id_for_email(email):
    result = save_performance_to_database.check_email_exist_or_not(email)
    #print(type(result))
    if isEmpty(result):
        return result['userid']
    else:
        return 0

#get_id_for_email('ssiva356@gmail.com')
#Method to get studetn details
def get_students_data():
    result = save_performance_to_database.get_all_students_data()
    return result
    
def isEmpty(dictionary):
   for element in dictionary:
     if element:
       return True
     return False

#method to store csv data to database
def store_data_to_database():
    file_access = open('FebWorkshops.csv','r')
    file_data = file_access.read()
    file_data_lines = file_data.split('\n')
    for line_nu in range(1,len(file_data_lines)-1):
        line_data = file_data_lines[line_nu].split(',')
        name = line_data[1]
        password = line_data[2]
        email = line_data[3]
        mobile = line_data[4]
        college = line_data[5]
        gender = line_data[6]
        batch = line_data[12]
        location = line_data[11]
        hackerrankid = line_data[7]
        githubid = line_data[8]
        linkedinid = line_data[9]
        save_performance_to_database.insert_data(name,password,email,mobile,college,gender,batch,location,hackerrankid,githubid,linkedinid)
        #print(email)
    file_access.close()
    return "success"
    #print(file_data_lines[37])
#store_data_to_database()

'''#Method to verify and store data to database from the registration page
def verify_and_store_data_to_database(user_form_details):
    user_email = user_form_details['email']
'''

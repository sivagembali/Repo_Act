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
#method to get data from url link with github_id and returns a json string
def get_github_data(github_id):
    #getting data from github using url and github_id
    #print(github_id)
    try:
        github_data = {}
        github_response_type_byte = requests.get("https://api.github.com/users/%s/repos"%github_id)
        github_response_data = json.loads(github_response_type_byte.content)
        for repository_data in range(len(github_response_data)):
            repo_id = github_response_data[repository_data]['id']
            repo_data = {}
            repo_data['name'] = github_response_data[repository_data]['name']
            repo_data['created_at']= github_response_data[repository_data]['created_at']
            repo_data['pushed_at'] = github_response_data[repository_data]['pushed_at']
            github_data[repo_id]= repo_data
        github_data_type_json_string = json.dumps(github_data)
        return github_data_type_json_string
    except Exception as exc:
        return "No Data Available"
#print(get_github_data('rajeunoia'))

#Method to get hackerrank and github data    
def get_data(user_id,hackerrank_id,github_id):
    hackerrank_and_github_data = {}
    hackerrank_and_github_data ['userid']= user_id
    hackerrank_and_github_data ['hackerrank_data'] = get_hackerrank_data(hackerrank_id)
    hackerrank_and_github_data ['github_data'] = get_github_data(github_id)
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

#Method to update all users status
def update_all_users_status():
    snumbers = save_performance_to_database.get_snumber_from_studentperformance_table()
    for data in snumbers:
        update_user_performance_data(data[0])
    return "Successfuly updated"

def update_all_ids(ids):
    email = ids['email_id']
    print("inside update_all_ids--",ids)
    student_info_dict = save_performance_to_database.check_email_exist_or_not(email)
    if(len(student_info_dict)):
        user_details={}
        user_details['studentinfo'] =  student_info_dict['studentinfo']
        user_details['hackerrankid'] = ids['hackerrank_id']
        user_details['github_id'] = ids['github_id']
        status = save_performance_to_database.update_ids_to_database(user_details)
        return status
    else:
        return "Email not registred"

    
'''#Method to verify and store data to database from the registration page
def verify_and_store_data_to_database(user_form_details):
    user_email = user_form_details['email']
'''
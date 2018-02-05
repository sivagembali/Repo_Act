import save_performance_to_database
import json
import requests

#Method to get data from url link with hackerrank_id and return a json string
def get_hackerrank_data(hackerrank_id):
    #getting data from hackerrank url which returns a byte type data
    hackerrank_response_type_byte = requests.get("https://www.hackerrank.com/rest/hackers/%s/submission_histories" %hackerrank_id)
    hackerrank_data_type_dict = json.loads(hackerrank_response_type_byte.content)
    hackerrank_data_type_json_string = json.dumps(hackerrank_data_type_dict)
    return hackerrank_data_type_json_string

#method to get data from url link with github_id and returns a json string
def get_github_data(github_id):
    #Dictionary to store the repository information from the github. Storing repository_name, created_date,updated_date,pushed_date
    github_data = {} 
    #getting data from github using url and github_id
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
    #print(data)
    return data
#update_user_performance_data(1)
from bigbrother.connector.jira import JiraBot as j
from bigbrother.model import create_issue

client = j()

def get_issue(key):
    response = client.getissue(key)

    if response:
        return create_issue(response)
    else:
        return None

def get_jql_results(jql, max_results=10):
    response = client.get_jql_results(jql, max_results)

    ret_list = []

    if response:
        for issue in response:
            ret_list.append(create_issue(issue))

        return ret_list

    else:
        return None
            
    


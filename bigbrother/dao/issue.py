from bigbrother.connector.jira import JiraBot as j
from bigbrother.connector.jira import make_configuration

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
            
    
def set_configuration(config):
    config = make_configuration(config['username'], config['password'])
    client._options = config
    


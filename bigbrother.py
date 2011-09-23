from bigbrother.dao.issue import get_jql_results

from time import sleep

def build_jql(assignee):
    return 'assignee=%s and status="In QA"' % assignee

assignees = ['fcobourn', 'utongbra', 'cknapp', 
'amatsaylo', 'ppoling', 'hstone', 'rholmes', 'jburton']


issue_dict = {}


# create the dict
for person in assignees:
    person_issues = get_jql_results(build_jql(person), 10)
    issue_dict[person] = person_issues


# print it out
for person, issues in issue_dict.iteritems():
    print person, "is currently working on:"

    # if the person is working on something
    if issues:
        for issue in issues:
            print "\t %s" % issue

    else:
        print "\t No items returned"




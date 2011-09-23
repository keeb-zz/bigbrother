from bigbrother.dao.issue import get_jql_results
from bigbrother.dao.issue import set_configuration

from os.path import expanduser
from os.path import join

from sys import exit
from re import compile
from time import sleep


def parse_config(f):
    ''' parses the configuration file in to a dict, takes in a file object '''
    valid_line = compile(r'(?P<key>[a-zA-Z0-9-_. ]+)=(?P<value>.*)')

    ret = {}

    for line in f:
        linematch = valid_line.match(line)
        if linematch:
            key = linematch.group('key').strip()
            value = linematch.group('value').strip()

            ret[key] = value

    return ret

def build_jql(assignee):
    return 'assignee=%s and status="In QA"' % assignee


home = expanduser('~/')

try:
    f = open(join(home, ".bigbrother"), 'r')
    configuration = parse_config(f)
except IOError, e:
    print ' there was an error: %s ' % e
    exit(1)

set_configuration(configuration)

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




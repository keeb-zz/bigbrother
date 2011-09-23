
def create_issue(di):
    ''' takes a RemoteIssue response from suds and creates an Issue object 
    
    currently only use the things we care about for bigbrother. As we start
    to create more and more tooling for JIRA this may reflect the full set
    of information available to us
    '''

    i = Issue()
    i.assignee = di.assignee
    i.key = di.key
    i.summary = di.summary

    return i


class Issue:
    ''' nothing special, just a class which we're going to create a couple
    attributes for'''


    def __init__(self):
        pass

    def __str__(self):
        return "%s - %s" % (self.key, self.summary)

    __repr__ = __str__


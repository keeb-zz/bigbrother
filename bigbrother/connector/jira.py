
import logging
from copy import deepcopy
from functools import wraps

from suds import WebFault
from suds.client import Client

log = logging.getLogger(__name__)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

class Configuration:
    def __init__(self):
        self.username = "fake"
        self.password = "fake"

def make_configuration(username, password):
    c = Configuration()
    c.username = username
    c.password = password
    return c

def requireslogin(func):
    '''Authentication/Error decorator for JiraBot class methods.'''
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.busted == True:
            return None
        if self.token == None:
            if not self.login():
                return None
        try:
            return func(self, *args, **kwargs)
        except WebFault, e:
            if "RemoteAuthenticationException" not in e.fault.faultstring:
                log.error('Unknown error from Jira: %s' % \
                        e.fault.faultstring)
                return None
            else:
                log.info('Auth token failed.')
                if self.login():
                    # try a 2nd time
                    try:
                        return func(self, *args, **kwargs)
                    except WebFault, e:
                        # new token didn't work, something is screwed
                        log.error('Unknown error from Jira: %s' %
                                e.fault.faultstring)
                        self.busted = True
                        return None
                else:
                    # can't log in, something is busted
                    self.busted = True
                    return None
    return wrapper


class JiraBot(object):
    '''Class to interop with JiraStudio through suds.

    Methods return None on failure.  The @requireslogin decorator, which wraps
    most of JiraBot's methods, takes care of authentication details and error
    logging.  If busted is set to True, JiraBot will not send requests.
    '''

    url = 'https://clairmail.jira.com/rpc/soap/jirasoapservice-v2?wsdl'
    _options = Configuration()
    token = None
    busted = False

    def __init__(self):
        self.client = Client(self.url)

    def login(self):
        if self.busted == True:
            return None
        try:
            log.info('Logging in to Jira')
            login = self.client.service.login(self._options.username,
                    self._options.password)
            self.token = str(login)
            return True
        except WebFault, e:
            if "RemoteAuthenticationException" in e.fault.faultstring:
                print e.fault.faultstring
                log.error('Failed to log in to Jira!')
                # credentials doesn't work, something is broken
                self.busted = True
                return None
            else:
                log.error('Failed due to unexpected error: %s' %
                        e.fault.faultstring)
                return None

    @requireslogin
    def getissue(self, key):
        return self.client.service.getIssue(self.token, key)

    @requireslogin
    def get_jql_results(self, jql, maxResults=0):
        jql_meth = self.client.service.getIssuesFromJqlSearch
        return jql_meth(self.token, jql, maxResults)




import requests
import requests_ntlm
import sys
import json
import os
import logging as logger

from Utilities import KennyLoggins
from Utilities import *
from ModularInput import *
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path
__author__ = 'ssalisbury'

_MI_APP_NAME = 'Sharepoint REST Input'
_APP_NAME = 'IA-sharepoint_rest'

_SPLUNK_HOME = make_splunkhome_path([""])

LOG_LEVEL = logger.INFO

log_location = make_splunkhome_path(['var', 'log', 'splunk', _APP_NAME])
log = logger.getLogger("{0}_modularinput".format(_APP_NAME))
if not os.path.isdir(log_location):
    os.mkdir(log_location)
output_file_name = os.path.join(log_location, '{}-modularinput.log'.format(_APP_NAME))
log.propogate = False
log.setLevel(LOG_LEVEL)
f_handle = handlers.RotatingFileHandler(output_file_name, maxBytes=25000000, backupCount=5)
formatter = logger.Formatter(
    '%(asctime)s %(levelname)s pid=%(process)d tid=%(threadName)s file=%(filename)s:%(funcName)s:%(lineno)d | %(message)s')
f_handle.setFormatter(formatter)
log.addHandler(f_handle)


## Eventually this stuff could be moved to Splunk config files
#site =
headers = {'Accept' : 'application/json;odata=verbose'}
params = "$filter=RequestWF eq 'Approved'&$expand=Applicant&$select=Applicant/Title, Email, Region, UserAccount, NameOfSystem, expirationDate"
wanted_keys = ['Title', 'Email', 'Region', 'UserAccount', 'NameOfSystem', 'expirationDate']

class SPModularInput(ModularInput):
    def __init__(self, **kwargs):
        ModularInput.__init__(self, **kwargs)

    def _validate_arguments(self, val_data):
        """
        :param val_data: The data that requires validation.
        :return:
        RAISE an error if the arguments do not validate correctly. The default is just "True".
        """
        return True

MI = SPModularInput(app_name=_APP_NAME, scheme={
    "title": "SharePoint Modular Input",
    "description": "Get stuff into Splunk from Sharepoint. Wooooo!",
    "args": [
        {"name": "username",
         "description": "This is the username for the Modular Input to consume information with.",
         "title": "Username",
         "required": True
         },
        {"name": "domain",
         "description": "This is the encrypted credential Realm to use when pulling the credential. Use the domain name of the user.",
         "title": "Credential Realm (Domain)",
         "required": True
         },
         {"name": "site",
          "description": "This is the Sharepoint site base url.",
          "title": "Sharepoint Site",
          "required": True
          },
        {"name": "list_name",
         "description": "This is the name of the list that will be pulled from SharePoint",
         "title": "List Name",
         "required": True
         }
    ]
})

def send_request(url, headers, domain, username, password):
    """
    Sends a request to the url with the credentials specified. Returns the final response
    """
    session = requests.Session()
    session.verify = False
    session.auth = requests_ntlm.HttpNtlmAuth(domain + '\\' + username,password)
    session.headers = headers
    response = session.get(url)
    return response

def create_url(list_name,site,params):
    url = "%s/_api/web/lists/GetByTitle('%s')/items?%s" % (site,list_name,params)
    return url

def process_response(data, wanted_keys):
    d = json.loads(data)
    for l in d[u'd'][u'results']:
        unfiltered_events = walk(l)
        events = {k: unfiltered_events[k] for k in wanted_keys}
    return events

def walk(node):
    items = {}
    def inner_walk(node):
        for key, value in node.items():
            if isinstance(value, dict):
                inner_walk(value)
            else:
                items[key] = value
        return items
    inner_walk(node)
    return items

def run():
    MI.start()
    log.info("action=start object=modular_input")
    try:
        list_name = MI.get_config("list_name")
        domain = MI.get_config("domain")
        username = MI.get_config("username")
        site = MI.get_config("site")
        #utils = Utilities(app_name=_APP_NAME, session_key=MI.get_config("session_key"))
        # ucred = utils.get_credential(MI.get_config("credential_realm"), username)
        url = create_url(list_name,site,params)
        s = send_request(url, headers, domain, username, ucred)
        #print(s)
        events = process_response(s.text, wanted_keys)
        for event in events:
            MI.print_event(event)
    except Exception, e:
        MI.print_error(e)
    MI.stop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            MI.scheme()
        elif sys.argv[1] == "--validate-arguments":
            MI.validate_arguments()
        elif sys.argv[1] == "--test":
            print('No tests for the scheme present')
        else:
            print('You giveth weird arguments')
    else:
        run()

    sys.exit(0)

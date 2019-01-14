import argparse
import getpass
import xml.etree.ElementTree as ET

import splunk.entity as entity
import splunk.rest as rest

parser = argparse.ArgumentParser(description='GT LDAP')
parser.add_argument('--update', action='store_true', )
args = parser.parse_args()
u = raw_input("Splunk User:")
p = getpass.getpass()
r, c = rest.simpleRequest(entity.buildEndpoint(['auth', 'login']), postargs={"username": u, "password": p})
root = ET.fromstring(c)
sessionkey = root[0].text
uri = entity.buildEndpoint(['storage', 'passwords'])
user = raw_input("REST User:")
host = raw_input("REST Host:")
password = getpass.getpass(prompt="REST Password:")
post_args = {"name": user, "realm": host, "password": password}
if args.update:
    uri = entity.buildEndpoint(['storage', 'passwords', "%s:%s:" % (host, user)])
    post_args = {"password": password}

r, c = rest.simpleRequest(uri, postargs=post_args, sessionKey=sessionkey)
print "Credential Created/Updated"

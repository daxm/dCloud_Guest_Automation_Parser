#!/usr/bin/python3

"""
This file will parse out the session.xml file for the Session ID and use that as the password
int the user-mapping.xml file for all the guacamole users.

"""

import xmltodict
import json
from lxml import etree
import os

#pathtosessionfile = '.'
pathtosessionfile = '/dcloud'
sessionfilename = 'session.xml'

#pathtousermappingfile = '.'
pathtousermappingfile = '/etc/guacamole/'
usermappingfilename = 'user-mapping.xml'

# Load the session file, convert from XML to an OrderedDict to a Dict.
with open(os.path.join(pathtosessionfile,sessionfilename), 'r') as file:
    dcloudsession = json.loads(json.dumps(xmltodict.parse(file.read())))

# I need the Session ID and the "oob" URL as they are needed to access the lab.
sessionid = dcloudsession['session']['id']
ooburl = dcloudsession['session']['translations']['translation']['name']

# Read in the user-mapping.xml file and update the guacamole users' password to the sessionid.
tree = etree.parse(os.path.join(pathtousermappingfile, usermappingfilename))
root = tree.getroot()
for child in root:
    child.attrib['password'] = sessionid

# Save the updated user-mapping.xml file
tree = etree.ElementTree(root)
tree.write(os.path.join(pathtousermappingfile,usermappingfilename))

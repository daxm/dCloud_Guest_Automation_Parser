#!/usr/bin/python3

"""
This file will parse out the session.xml file for the Session ID and use that as the password
int the user-mapping.xml file for all the guacamole users.

This file's source is from https://github.com/daxm/dCloud_Guest_Automation_Parser.
"""

import xmltodict
import json
from lxml import etree
import os
import sys

# Fix the path variable to match your setup.
pathtosessionfile = '.'
#pathtosessionfile = '/dcloud'
sessionfilename = 'session.xml'

pathtousermappingfile = '.'
#pathtousermappingfile = '/etc/guacamole/'
usermappingfilename = 'user-mapping.xml'

# Load the session file, convert from XML to an OrderedDict to a Dict.
sessionfile = os.path.join(pathtosessionfile, sessionfilename)
try:
    with open(sessionfile, 'r') as file:
        dcloudsession = json.loads(json.dumps(xmltodict.parse(file.read())))
except:
    print("Error: Cannot open %s.  Exiting..." % (sessionfile))
    exit(1)

# I need the Session ID and the "oob" URL as they are needed to access the lab.
sessionid = dcloudsession['session']['id']
ooburl = dcloudsession['session']['translations']['translation']['name']

# Read in the user-mapping.xml file and update the guacamole users' password to the sessionid.
usermappingfile = os.path.join(pathtousermappingfile, usermappingfilename)
try:
    tree = etree.parse(usermappingfile)
    root = tree.getroot()
    for child in root:
        child.attrib['password'] = sessionid

    # Save the updated user-mapping.xml file
    tree = etree.ElementTree(root)
    tree.write(usermappingfile)
except:
    print("Error: Cannot open %s.  Exiting..." % (usermappingfile))
    exit(1)

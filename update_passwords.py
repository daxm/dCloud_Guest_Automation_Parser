#!/usr/bin/python3

"""
This file will parse out the session.xml file for the Session ID and use that as the password
int the user-mapping.xml file for all the guacamole users.

This file's source is from https://github.com/daxm/dCloud_Guest_Automation_Parser.
"""

import xmltodict
import json
import lxml
import os

# Fix the path variable to match your setup.
session_file_path = '.'
#pathtosessionfile = '/dcloud'
session_file_name = 'session.xml'

# Load the session file, convert from XML to an OrderedDict to a Dict.
session_file = os.path.join(session_file_path, session_file_name)

with open(session_file, 'r') as file:
    dcloud_session = json.loads(json.dumps(xmltodict.parse(file.read())))

# I need the Session ID and the "oob" URL as they are needed to access the lab.
session_id = dcloud_session['session']['id']
oob_url = dcloud_session['session']['translations']['translation']['name']

user_mapping_file_path = '.'
#pathtousermappingfile = '/etc/guacamole/'
user_mapping_file_name = 'user-mapping.xml'

# Read in the user-mapping.xml file and update the guacamole users' password to the session_id.
user_mapping_file = os.path.join(user_mapping_file_path, user_mapping_file_name)

tree = lxml.etree.parse(user_mapping_file)
root = tree.getroot()
for child in root:
    child.attrib['password'] = session_id

# Save the updated user-mapping.xml file
tree = lxml.etree.ElementTree(root)
tree.write(user_mapping_file)

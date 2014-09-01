# This fetches the current poems from a private Drupal site
import xmlrpcsettings
import xmlrpclib
import re
import json
import urllib

assert xmlrpcsettings.ursite
assert xmlrpcsettings.inbookurl

proxy = xmlrpclib.Server(xmlrpcsettings.ursite)

open_url = urllib.urlopen(xmlrpcsettings.inbookurl)
nds=json.load(open_url)
items = nds['Items']
inbook = []
for i in items:
    inbook.append( proxy.node.retrieve(i['node']['nid']) )
assert len(inbook)==30


# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <rawcell>

# This notebook is used to generate the Urdu, Devanagari, and transliteration versions of the poem's in the appendix to my book, I Too Have Some Dreams, http://seanpue.com/itoohavesomedreams/

# <codecell>

# This fetches the current poems from a private Drupal site accessed via xmlrpc

import xmlrpcsettings # this holds a few private settings
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

# <codecell>

def clean_trans(s):
    s = s.replace('--',u'—')
    s = s.replace(' -o- ','-o-')
    return s
def cap_trans(s):
    if s[0]==u'ḥ':
        s=u'Ḥ'+s[1:]
    return s

# <codecell>

for n in inbook:
    # first, transliteration
    title = cap_trans(clean_trans(n['field_title_transliterated']['und'][0]['value']))
    
    print title

# <codecell>

n['field_title_transliterated']['und'][0]['value']

# <codecell>

s.


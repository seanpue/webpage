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

print inbook[0]['field_title_urdu']['und'][0]['value']#: {'und': [{'value'

# <codecell>

def clean_trans(s):
    s = s.replace('--',u'—')
    s = s.replace(' -o- ','-o-')
    s = s.replace('\t','    ')# -o- ','-o-')
    return s

def cap_trans(s):
    if s[0]==u'ḥ':
        s=u'Ḥ'+s[1:]
    return s

# <codecell>

for n in inbook:
    # first, transliteration
    trans_title = cap_trans(clean_trans(n['field_title_transliterated']['und'][0]['value']))
    urdu_title = n['field_title_urdu']['und'][0]['value']
    print trans_title, urdu_title

# <codecell>

import datetime
import dateutil
def current_time(tzinfo=None):
    if tzinfo is not None:
        dt = datetime.datetime.now(tzinfo)
    else:
        dt = datetime.datetime.now(dateutil.tz.tzlocal())
    return dt

datetime.datetime.now()

# <codecell>

import datetime
utc_datetime = datetime.datetime.utcnow()
utc_datetime.strftime("%Y-%m-%d %H:%M:%S")+" UTC"

# <codecell>

inbook[0]['field_text_urdu']['und'][0]['value']

# <codecell>

import datetime
import os
import codecs


def generate_rst(n,poem_id): 
    '''
    generates RestructuredText string from Drupal node
    n = drupal node
    poem_id = id in book, starting at 1
    
    Model:
      
    .. title: test post
    .. slug: test-post
    .. date: 2014-09-01 03:10:12 UTC
    .. tags: 
    .. link: 
    .. description: 
    .. type: text

    '''
#    n=inbook[25]

    text_trans=clean_trans(n['field_text_transliterated']['und'][0]['value'])
    text_trans_lines = text_trans.split('\n')
    text_trans_lines = ['| '+s for s in text_trans_lines]
    trans_title = cap_trans(clean_trans(n['field_title_transliterated']['und'][0]['value']))
    text_transliterated_rst = '\n'.join(text_trans_lines)
    
    
    utc_datetime = datetime.datetime.utcnow()
    slug = 'itoohavesomedreams/poem_'+str(poem_id)    
    time_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")+" UTC"
    
    rst_text = '.. title: %s\n'       % (u'§'+str(poem_id)+'. '+trans_title)
    rst_text+= '.. slug: %s\n'        % slug
    
    rst_text+= '.. date: %s\n'        % time_string
    rst_text+= '.. tags: %s\n'        % 'poem itoohavesomedreams rashid'
    rst_text+= '.. link: %s\n'        % '' # what is this?
    rst_text+= '.. description: %s\n' % ('transliterated version of "'+trans_title+'"')
    rst_text+= '.. type: text'+'\n'
    rst_text+= '\n'
    rst_text+= u'\n\n'    
    rst_text+= text_transliterated_rst
    rst_text+= u'\n\n\u2403\n'#\u2403
#    print rst_text

    assert os.path.isdir('../itoohavesomedreams')
    filename_en = '../'+slug+'.rst'
    with codecs.open(filename_en,'w','utf-8') as f: # physical location does not matter though for slug
        f.write(rst_text)

        
def generate_ur_rst(n,poem_id): 
    '''
    generates RestructuredText string from Drupal node
    n = drupal node
    poem_id = id in book, starting at 1
    
    Model:
      
    .. title: test post
    .. slug: test-post
    .. date: 2014-09-01 03:10:12 UTC
    .. tags: 
    .. link: 
    .. description: 
    .. type: text

    '''
#    n=inbook[25]

    text_ur =n['field_text_urdu']['und'][0]['value']
    text_ur_lines = text_ur.split('\n')
    text_ur_lines = ['| '+s for s in text_ur_lines]
    text_ur_rst = '\n'.join(text_ur_lines)
    trans_title = cap_trans(clean_trans(n['field_title_transliterated']['und'][0]['value']))    
    ur_title = n['field_title_urdu']['und'][0]['value']
    utc_datetime = datetime.datetime.utcnow()
    slug = 'itoohavesomedreams/poem_'+str(poem_id)    
    time_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")+" UTC"
    
    rst_text = '.. title: %s\n'       % (u'§'+str(poem_id)+u'ـ '+ur_title)
    rst_text+= '.. slug: %s\n'        % slug
    
    rst_text+= '.. date: %s\n'        % time_string
    rst_text+= '.. tags: %s\n'        % 'poem itoohavesomedreams rashid'
    rst_text+= '.. link: %s\n'        % '' # what is this?
    rst_text+= '.. description: %s\n' % ('Urdu version of "'+trans_title+'"')
    rst_text+= '.. type: text'+'\n'
    rst_text+= '\n'
    rst_text+= u'\n\n'    
    rst_text+= text_ur_rst
    rst_text+= u'\n\n\u2403\n'#\u2403
 #   print rst_text

    assert os.path.isdir('../itoohavesomedreams')
    filename_en = '../'+slug+'.ur'+'.rst' # format is : title.languageid.rst
    
    with codecs.open(filename_en,'w','utf-8') as f: # physical location does not matter though for slug
        f.write(rst_text)
        
         
    
    

# <codecell>

def index_link(n,n_id):
    trans_title = cap_trans(clean_trans(n['field_title_transliterated']['und'][0]['value']))
    print u'  §'+str(n_id)+u'. `'+trans_title+u' <poem_'+str(n_id)+u'/>'+'`_'+'\n'


# <codecell>



for n_id, n in enumerate(inbook):
    generate_rst(n,n_id+1)
    generate_ur_rst(n,n_id+1)
    index_link(n,n_id+1)
    

# <codecell>


# <codecell>

(u'§'+str(poem_id)+u'ـ '+ur_title)

# <codecell>


# <codecell>


# <codecell>



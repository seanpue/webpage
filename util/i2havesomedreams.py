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
    return u''+s

def cap_trans(s):
    if s[0]==u'ḥ':
        s=u'Ḥ'+s[1:]
    return u''+s

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

import datetime
import os
import codecs


def generate_rst(n,poem_id,nodes): 
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
    def get_title_trans(n):
        return u''+cap_trans(clean_trans(n['field_title_transliterated']['und'][0]['value']))
    text_trans = clean_trans(n['field_text_transliterated']['und'][0]['value'])
    
    text_trans_lines = text_trans.split('\n')
    text_trans_lines = ['| '+s for s in text_trans_lines]
    trans_title = get_title_trans(n)
    text_transliterated_rst = '\n'.join(text_trans_lines)
    
    admonition = """
.. admonition:: I Too Have Some Dreams: N. M. Rashed and Modernism in Urdu Poetry

  A translation of this Urdu poem by N. M. Rashed as well as this transliteration appears in the
  appendix of *I Too Have Some Dreams*. Then transliteration is intended for
  people who can understand Urdu/Hindi or related languages. I hope to soon 
  add performances of these poems as well. 
  
  .. link_figure:: /itoohavesomedreams/
        :title: I Too Have Some Dreams Resource Page
        :class: link-figure
        :image_url: /galleries/i2havesomedreams/i2havesomedreams-small.jpg
        
"""

    utc_datetime = datetime.datetime.utcnow()
    slug = 'itoohavesomedreams/poem_'+str(poem_id)    
    time_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")+" UTC"
    
    rst_text = u'.. title: %s\n'       % (u'§'+str(poem_id)+'. '+trans_title)
    rst_text+= u'.. slug: %s\n'        % slug
    
    rst_text+= u'.. date: %s\n'        % time_string
    rst_text+= u'.. tags: %s\n'        % 'poem itoohavesomedreams rashid'
    rst_text+= u'.. link: %s\n'        % '' # what is this?
    rst_text+= u'.. description: %s\n' % ('transliterated version of "'+trans_title+'"')
    rst_text+= u'.. type: text'+'\n'
    rst_text+= u'\n'
    rst_text+= u'\n\n'    
    rst_text+= text_transliterated_rst
    rst_text+= u'\n\n'
    add_later=u''
    if poem_id>1:
        rst_text+=u'|left arrow link|_\n'
        next_poem = nodes[poem_id-2]
        prev_title = get_title_trans(nodes[poem_id-2])
        add_later+=u"\n.. |left arrow link| replace:: :emoji:`arrow_left` §{poem_id}. {poem_title} ".format(
            poem_id=poem_id-1,
            poem_title=prev_title#u''+get_title_trans(nodes[poem_id-2]) # could adjust -1 in def
        )
        add_later+='\n.. _left arrow link: /itoohavesomedreams/poem_{poem_id}\n'.format(poem_id=poem_id-1)
    if poem_id<len(nodes):
        rst_text+='\n|right arrow link|_\n'
        add_later+=u"\n.. |right arrow link| replace::  §{poem_id}. {poem_title} :emoji:`arrow_right` ".format(
            poem_id=poem_id+1,
            poem_title=get_title_trans(nodes[poem_id])#prev_title#u''+get_title_trans(nodes[poem_id-2]) # could adjust -1 in def
        )

        add_later+='\n.. _right arrow link: /itoohavesomedreams/poem_'+str(poem_id+1)+'\n'
    rst_text+='\n\n'+add_later+admonition;
#    rst_text+= u'\n\n\u2403\n'#\u2403
#    print rst_text

    assert os.path.isdir('../itoohavesomedreams')
    filename_en = '../'+slug+'.rst'
    with codecs.open(filename_en,'w','utf-8') as f: # physical location does not matter though for slug
        f.write(rst_text)

        
def generate_ur_rst(n,poem_id,nodes): 
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
    def get_ur_title(n):
        return n['field_title_urdu']['und'][0]['value']
    text_ur =n['field_text_urdu']['und'][0]['value']
    text_ur_lines = text_ur.split('\n')
    text_ur_lines = ['| '+s for s in text_ur_lines]
    text_ur_rst = '\n'.join(text_ur_lines)
    trans_title = cap_trans(clean_trans(n['field_title_transliterated']['und'][0]['value']))    
    ur_title = get_ur_title(n)#n['field_title_urdu']['und'][0]['value']
    utc_datetime = datetime.datetime.utcnow()
    slug = 'itoohavesomedreams/poem_'+str(poem_id)    
    time_string = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")+" UTC"
    
    rst_text = u'.. title: %s\n'       % (u'§'+str(poem_id)+u'ـ '+ur_title)
    rst_text+= u'.. slug: %s\n'        % slug
    
    rst_text+= u'.. date: %s\n'        % time_string
    rst_text+= u'.. tags: %s\n'        % 'poem itoohavesomedreams rashid'
    rst_text+= u'.. link: %s\n'        % '' # what is this?
    rst_text+= u'.. description: %s\n' % ('Urdu version of "'+trans_title+'"')
    rst_text+= u'.. type: text'+'\n'
    rst_text+= u'\n'
    rst_text+= u'\n\n'    
    rst_text+= text_ur_rst+'\n\n'
#    rst_text+= u'\n\n\u2403\n'#\u2403
 #   print rst_text
    add_later=u''
    admonition=u"""
.. admonition:: I Too Have Some Dreams: N. M. Rashed and Modernism in Urdu Poetry

  یہ ن م راشد کی نظم ہے ـ اس کا انگریزی ترجمہ اور ٹرانزلٹریشن میری کتاب
  کے ضمیمہ میں مل سکتا ہےـ اردو
  پڑھنے والوں کے لئے یہ پیج پیش کیا گیا ہےـ نستعلیق میں
  دکھانے کے لئے 
  `جمیل نوری نستعلیق فانٹ`_  انسٹال کیجئے.


  .. link_figure:: /itoohavesomedreams/
        :title: I Too Have Some Dreams Resource Page
        :class: link-figure
        :image_url: /galleries/i2havesomedreams/i2havesomedreams-small.jpg
        
.. _جمیل نوری نستعلیق فانٹ: http://ur.lmgtfy.com/?q=Jameel+Noori+nastaleeq
 

"""
    if poem_id>1:
      rst_text+=u'\n|right arrow link|_\n'
      next_poem = nodes[poem_id-2]
      prev_title = get_ur_title(nodes[poem_id-2])
      add_later+=u"\n.. |right arrow link| replace:: :emoji:`arrow_right` §{poem_id}. {poem_title}  ".format(
          poem_id=poem_id-1,
          poem_title=prev_title#u''+get_title_trans(nodes[poem_id-2]) # could adjust -1 in def
      )
      add_later+=u'\n.. _right arrow link: /itoohavesomedreams/poem_{poem_id}\n'.format(poem_id=poem_id-1)
    if poem_id<len(nodes):
      rst_text+=u'\n|left arrow link|_\n'
      add_later+=u"\n.. |left arrow link| replace::   §{poem_id}. {poem_title} :emoji:`arrow_left` ".format(
          poem_id=poem_id+1,
          poem_title=get_ur_title(nodes[poem_id])#prev_title#u''+get_title_trans(nodes[poem_id-2]) # could adjust -1 in def
      )
      add_later+=u'\n.. _left arrow link: /itoohavesomedreams/poem_'+str(poem_id+1)+'\n'
  
    rst_text+='\n\n'+add_later+admonition;
    
        
    assert os.path.isdir('../itoohavesomedreams')
    filename_en = '../'+slug+'.ur'+'.rst' # format is : title.languageid.rst
    
    with codecs.open(filename_en,'w','utf-8') as f: # physical location does not matter though for slug
        f.write(rst_text)
        
         
    
    

# <codecell>

def index_link(n,n_id):
    trans_title = cap_trans(clean_trans(n['field_title_transliterated']['und'][0]['value']))
    print u'  `§'+str(n_id)+u'. '+trans_title+u' <poem_'+str(n_id)+u'/>'+'`_'+'\n'


# <codecell>



for n_id, n in enumerate(inbook):
    generate_rst(n,n_id+1,inbook)
    generate_ur_rst(n,n_id+1,inbook)#,inbook)
    index_link(n,n_id+1)
    

# <codecell>


# <codecell>


# <codecell>



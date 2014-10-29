import re


def load_yaml(filename):
    """
    Reads any yaml file and returns it as object.
    """
    import yaml
    stream = file(filename)
    return yaml.load(stream)

debug=False
        
import unicodedata
def unescape_unicode_charnames(s):
    """
    Takes \N{charname} in production rule and turns to Unicode string.
    """
    
    def get_unicode_char(matchobj):
#            """
#            Returns Unicode character of \N{character name}
#            """
#           if debug: print "Trying "+matchobj+"in get_unicode_char"
        s = matchobj.group(0)
        m = re.match(r'\\N{(.+)}',s)
        char = unicodedata.lookup(m.group(1))
        return char

    return re.sub(r'\\N{.+?}',get_unicode_char,s)

def compare_rules(x,y):
    """
    Compares rules and sees which has more tokens or conditions (prev, next)
    """
    
    diff = 10*(len(y['tokens'])-len(x['tokens']))   
    if diff != 0:
        return diff
    (x_conds, y_conds) = (0,0)
    for cond in ('prev','next'):
        if cond in x: x_conds +=len(x[cond])
        if cond in y: y_conds +=len(y[cond])
    for cond in ('prev_classes', 'next_classes'):
        if cond in x: x_conds += len(x[cond])
        if cond in y: y_conds += len(y[cond])
    return y_conds - x_conds # see if one has  more <classes>


def onmatch_rules_from_yaml_data(rules_raw):
    ''' Some quick code to generate the onmatch rules. It only relies on classes '''
    ''' returns a tuple ( (left_classes,right_classes) , prod)
        rules are classes '''
    onmatch_rules = [] # clean list of rule
#    print "rules_r is"+str(rules_raw)
    debug=True

    match_rules = []
    for key in rules_raw:
        assert len(key)==1
        rule = key.keys()[0]
        prod_orig = key[rule]
        prod = unescape_unicode_charnames(prod_orig)


        print rule
        m= re.match('([^+]+)\+([^+]+)$',rule)
        assert m
        
        l = m.group(1) #left
        r =m.group(2)  #right

        cl_l=re.findall('(?<=<)[^<]+(?=>)',l)
        cl_r=re.findall('(?<=<)[^<]+(?=>)',r)
        onmatch_rules.append(( (cl_l, cl_r) , prod ))
    return(onmatch_rules)
    
def rules_from_yaml_data(rules_raw):
    """
    Returns sorted and usable parser rules from yaml file. 

    rules_raw is a dictionary (loaded from yaml):
        key: <previous token class> token token <next token class> 
        value: production

    previous class and next class of token are optional. 
    The production allows \N{unicode char name} strings.

    Output of return is list of rules containing:
        prev_class: previous token class [optional, will look behind prev]
        prev:       previous tokens [optional]
        tokens:     list of tokens
        next:       next token class [optional]
        next_class: next token class [option, will look ahead of next]
        production: string production

    """
    

        # load and prepare rules
    
    rules = [] # clean list of rule
#    print "rules_r is"+str(rules_raw)
    for key in rules_raw:
        if debug: print "key is "+key+" = "+rules_raw[key]
        rule = {}           #1       #2        #3

#        if debug: print "trying "+key+" in rules_from_yaml_data()"
        """
        m = re.match(r'(?:<(.+?)> )?(.+?)(?: <(.+?)>)?$', key,re.S)

        if m.group(1): rule['prev']   = m.group(1)
        rule['tokens'] = m.group(2).split(' ')
        if m.group(2)==' ':
            rule['tokens'] = [' '] # override for space ' '
        if m.group(3): rule['next']   = m.group(3)
        rule['production'] = unescape_unicode_charnames(rules_raw[key])
        """
        _  ='(?:'   
        _ +='\('
        _ +='((?:\s?<.+?>\s+)+)?'# '(?:\s?<(.+?)>\s+)?' # group 1, prev class (in brackets indicating cluster)
        _ +='(.+?)\s?' # group 2, prev tokens (to be split)
        _ +='\) '
        _ +='|' # either a cluster or a particular previous class (Could add additional support, e.g. class or paretic.
        _ +='((?:\s?<.+?>\s+)+)?' # group 3, prev class (not in cluster)
        _ +=')?'
        _ += '(.+?)' # group 4, tokens
        _ += '(?:' # cluster for following tokens, clusters 
        _ += ' \('
        _ += '\s?(.+?)' # group 5, next tokens
        _ += '((?:\s?<.+?>\s+?)+)?' # group 6, next class
        _ += '\s?\)'
        _ += '|'
        _ += ' ((?:<.+?>\s?)+)?' # group 7, follo
        _ += ')?$'
        
        m = re.match (_, key, re.S)
        assert (m is not None)
        if m.group(1): rule['prev_classes'] = re.findall('<(.+?)>',m.group(1))
        if m.group(2): rule['prev_tokens'] = m.group(2).split(' ')
        if m.group(3): rule['prev_classes'] =  re.findall('<(.+?)>',m.group(3))
        if m.group(4)==' ':
            rule['tokens'] = ' '
        else:
            rule['tokens'] = m.group(4).split(' ')
        if m.group(5): rule['next_tokens'] = m.group(5).split(' ')
        if m.group(6): rule['next_classes'] = re.findall('<(.+?)>',m.group(6))
        if m.group(7): rule['next_classes'] = re.findall('<(.+?)>',m.group(7))
            
        rule['production'] = unescape_unicode_charnames(rules_raw[key])
        if debug:print rule
        if debug:print '----'
        rules.append(rule)

    return rules

debug=False
class Parser:
    error_on_last = False
    last_string = ''
    error_string = ''
    def generate_token_match_string(self):
        tokens = self.tokens.keys()
        sorted_tokens = sorted(tokens, key=len, reverse=True)
        escaped_tokens = map(re.escape, sorted_tokens)
        tokens_re_string = '|'.join(escaped_tokens)+'|.' # grab unknowns
        return tokens_re_string

    def generate_token_match_re(self):
        '''
        Create regular expression from Parser.tokens sorted by length

        Adds final "." in case nothing found
        '''

        tokens = self.tokens.keys()
        sorted_tokens = sorted(tokens, key=len, reverse=True)
        escaped_tokens = map(re.escape, sorted_tokens)
        tokens_re_string = '|'.join(escaped_tokens)+'|.' # grab unknowns
        return re.compile(tokens_re_string, re.S)

    def tokenize(self,input):
        return self.token_match_re.findall(input)

    def parse(self,input,on_error='',on_error_additional='',return_all_matches=False, debug=False):
        #reset error-catching variables
        self.last_string = input
        self.error_string = ''
        self.error_on_last = False
        self.parse_details = []

        output = ''
        tkns = self.token_match_re.findall(input)
        t_i = 0              # t_i counter for token position in list
        while t_i<len(tkns): # while in range of tokens in string
            matched = False
            for rule_id,rule in enumerate(self.rules):
                try:
                    r_tkns = []
                    if ('prev_tokens' in rule): 
                        i_start = t_i-len(rule['prev_tokens'])
                        r_tkns += rule['prev_tokens']
                        #'print problem in '+str(rule)
                    else:
                        i_start = t_i
                    r_tkns +=rule['tokens']                
                    if 'next_tokens' in rule:
                        r_tkns += rule['next_tokens']
                    if all(r_tkns[i] == tkns[i_start+i] for i in range(len(r_tkns)) ):
                    #    pdb.set_trace()  
                        if 'prev_classes' in rule:
                            prev_classes = rule['prev_classes'][::-1] # reverse these
                            if i_start - len(prev_classes) < -1: 
                                continue
                            to_match =([' ']+tkns)[i_start+1-len(prev_classes):i_start+1][::-1]
                             #tkns[i_start-len(prev_classes):i_start][::-1]+[' '] 
                            
                            if not all(prev_classes[i] in self.tokens[to_match[i]] for i in range(len(prev_classes))): 
                                continue
                                
                                
#                        if 'prev_class' in rule: # if rule has a prev class
#                            if i_start==0: 
##                                # if at start of string, allow for word break
 ##                               prev_token = ' '
   #                         else:
    #                            prev_token = tkns[i_start-1]                        #    
       #                     if not(rule['prev_class'] in self.tokens[prev_token]):
      #                          continue
                                
                        if 'next_classes' in rule:
                            next_classes = rule['next_classes']
                            if i_start + len(r_tkns)+len(next_classes) > len(tkns)+1:
                                continue
                                
                            to_match = tkns[i_start+len(r_tkns):i_start+len(r_tkns)+len(next_classes)] + [' ']
                            if not all(next_classes[i] in self.tokens[to_match[i]] for i in range(len(next_classes))): 
                                continue
                            #prev_classes:i_start]+[' ']
                            #if i_start+len(r_tkns)==len(tkns): # if end of string
#                                next_token = ' '
#                            else:
#                                next_token = tkns[i_start+len(r_tkns)]
#                            if not next_token in self.tokens:
#                                next_token = ' ' # in case it's missing (SHOULD THIS BE ADDED ABOVE?)
                            #if not(rule['next_class'] in self.tokens[next_token])#:
                         #       continue
                        # We did it!
                        if debug==True:
                            print "matched "+str(rule)
                        matched = True

                        self.parse_details.append({'tokens':rule['tokens'], 'start':t_i, 'rule':rule, 'rule_id':rule_id})
                        
                        # add onmatch rules...
                        if self.onmatch_rules:
#                            pdb.set_trace()  
                            mtkns = [' ']+tkns+[' ']
                            mt_i = t_i+1
                            for m in self.onmatch_rules:
        #                        pdb.set_trace()
                                (classes,p)=m
                                (l_c,r_c)=classes
                                # try left match
                                if mt_i < len(l_c) or mt_i+len(r_c)>len(mtkns):
                                    continue
#ln                                pdb.set_trace()
                                
#                                my_range = range(t_i-len(l_c),t_i+(r_c))
                                
                                classes_to_test_l = [self.tokens[c] for c in mtkns[mt_i-len(l_c):mt_i]]
                                
                                classes_to_test_r = [self.tokens[c] for c in mtkns[mt_i:mt_i+len(r_c)]]
                                
                                if not all(l_c[i] in classes_to_test_l[i] for i in range(len(l_c))):
                                    continue
                                if not all(r_c[i] in classes_to_test_r[i] for i in range(len(r_c))):
                                    continue
   #                             print 'found match rule!!!'
#                                pdb.set_trace()                                
                                output += p
                                break # break out of for loop
                                
                        
                        output += rule['production']                        
                        t_i += len(rule['tokens']) 

                        
                        break
                except IndexError:
                    continue
            if matched==False:
                import unicodedata
                curr_error = 'no match at token # '+str(t_i)+': '+tkns[t_i]+" "
                try:
                  for c in tkns[t_i]:
                    curr_error += unicodedata.name(unichr(ord(c)))+" "
                except TypeError:
                  curr_error += "TYPE ERROR HERE!!!!"
                curr_error += ' [' + on_error_additional + ']'
                if on_error=='print':
                    print curr_error
                self.error_on_last = True
                self.error_string +=curr_error+"\n"
                self.parse_details.append({'tokens':tkns[t_i], 'start':t_i, 'rule':None}) # save error
                prev_token=' ' # reset
                t_i += 1
        return output

    def match_all_at(self,tkns,t_i):
        """    return {rule_id:1, # look up for rule
                start:0, # index of match
                tokens:x,
                production: }
        """
        matches = ''
        output = []
        #if tkns[-1]!='b':
        #    tkns.append('b')
        for rule_id,rule in enumerate(self.rules):
            #pGrint rule['tokens']
            #pdb.set_trace()
            try:
                r_tkns = [] # array of all tokens to match (including rule's [prev_tokens]&[next_tokens]
                if ('prev_tokens' in rule):
                    i_start = t_i-len(rule['prev_tokens'])
                    r_tkns += rule['prev_tokens']
                else:
                    i_start = t_i
                r_tkns +=rule['tokens']
                if 'next_tokens' in rule:
                    r_tkns += rule['next_tokens']
                if all(r_tkns[i] == tkns[i_start+i] for i in range(len(r_tkns)) ):
                    if 'prev_classes' in rule: # if rule has a prev class
                        if i_start==0:
                            # if at start of string, allow for word break
                            prev_token = 'b'
                        else:
                            prev_token = tkns[i_start-1]
                        if not(rule['prev_class'] in self.tokens[prev_token]):
                            continue
                    if 'next_class' in rule:
                        if i_start+len(r_tkns)==len(tkns): # if end of string
                            next_token = 'b'
                        else:
                            next_token = tkns[i_start+len(r_tkns)]
                        if not next_token in self.tokens:
                            next_token = 'b' # in case it's missing (SHOULD THIS BE ADDED ABOVE?)
                        if not(rule['next_class'] in self.tokens[next_token]):
                            continue
                    # We did it!
                    matched = True
                    output.append( {'rule_id':rule_id, 'tokens':rule['tokens'], 'start': t_i, 'rule':rule} )
                    
            except IndexError:
                continue
        return output
    
    def __init__(self, yaml_file='', data=None):
        
        if data != None:
            print "You got data, son."
        elif yaml_file != '':
            data = load_yaml(yaml_file)
        else: 
            assert data is not None
        self.rules = rules_from_yaml_data(data['rules']) # specifically YAML here
        if 'onmatch' in data:
            self.onmatch_rules = onmatch_rules_from_yaml_data(data['onmatch'])
        else:
            self.onmatch_rules = False

        rules = self.rules
        rules.sort(cmp=compare_rules)
        self.tokens = data['tokens']
        self.token_match_re = self.generate_token_match_re()

if __name__ == '__main__':
    import pdb
    pdb.set_trace()  
    p = Parser('devanagari.yaml')
    pdb.set_trace()  
    print(p.parse("tah"))#rah_rau))o;n"))#taa tah tii itihaas"))
    print 'hi'
    #print_scan(s,knownOnly=False)
    #scn = scan(" ko))sab paimaane be-.sarfah jab siim-o-zar miizaan")#be-;xvudii le ga))ii kahaa;n mujh ko")#der se inti:zaar hai apnaa")# faryaadii hai kis kii sho;xii-e ta;hriir kaa")
    #print_scan(scn,knownOnly=False)


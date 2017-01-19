import pdb
import numpy as np
import random
import sys
import os
import regex as re
import itertools
import datetime
import pickle 


debug = True 
    

# redefines
def Join  (list_):
  return '\n'.join(list_)
def Range_(list_):
  if type(list_) is list:
    return xrange(0, len(list_))
  elif type(list_) is int:
    return xrange(0, list_)
  elif type(list_) is str:
    return xrange(0, len(list_))
def Indent(input_):
    if type(input_) == str:
        return re.sub('\n','\n    ', input_) 
    elif type(input_) == list:
        for each_item in Range_(input_):
            input_[each_item] = re.sub('\n','\n    ', input_[each_item]) 
        return input_ 
def Load  (string_):
  exec ('''global '''+string_+'''\n'''+string_ +"""= pickle.load(open(\""""+string_+'.pickle","rb"))')
def Save  (string_):
  exec ('''pickle.dump('''+string_+''', open("'''+string_+'''.pickle","wb"))''')
def exists(var_ , value=''):
    # if var_ is a dictionary 
    if type(var_) == dict:
        # value needs to be a string
        # returns T or F 
        try:
            exec('''var_'''+value)
            return True
        except KeyError:
            return False
    elif type(value) == int: 
        # value needs to be a string
        # returns T or F 
        try:
            var_
            return True
        except IndexError:
            return False
    else:
        # value needs to be a string
        # returns T or F 
        try:
            var_
            return True
        except NameError:
            return False
def PrintDict            (dict_ , indent=8 ,  depth_=-1):
    depth_ = depth_ + 1 
    this_level = depth_
    for each in dict_:
        if type(dict_ [ each ]) == dict:
            print ' '*indent*this_level + str(each)+ ' '*(12 - len(str(each))) + ':'
            PrintDict( dict_ [ each ] , indent  , depth_ )
        else:
            print ' '*indent*this_level + str(each) + ' '*(12 - len(str(each))) + ': ' + str(dict_[each])
def PrintList            (list_ , indent=8             ):
    for each in list_:
        if type(each) == list:
            for inside_each in each:
                print inside_each , 
        else:
            print ' '*indent+ str(each) 
def RemoveDuplicatesFrom (original_list): 
  seen = set()
  seen_add = seen.add
  return [x for x in original_list if not (x in seen or seen_add(x))]
def Is__RegexIn__String  (regexstring,string): 
    # the stupid $ doesn't actually match the end 
    # at least it doesn't when there's a \n at the end 
    # so to get around this, I append (?![\s\S]) to the end
    if regexstring[-1] == '$' and regexstring[-2] != '\\':
        regexstring = regexstring + r'(?![\s\S])'
    output = re.search(regexstring,string) != None 
    return output
def CombineTwoDictionarys(x,y):
    z = x.copy()
    z.update(y)
    return z
def LocationOf__RegexStartIn__String    (regex,string):
  group_setup = re.search(regex,string)
  return group_setup.start()
def LocationOf__RegexEndIn__String      (regex,string):
  group_setup = re.search(regex,string)
  return group_setup.end()
def ReturnRandomNumberStringThatsNotIn__(input_):
          if type(input_) is list:
            string_ = "\n".join(input_)
          elif type(input_) is dict:
            string_ = "\n".join(input_.values())
          elif type(input_) is str:
            string_ = input_ 
          else:
            return None 
          random_placeholder     = str(random.randrange(10000000))
          while Is__RegexIn__String( random_placeholder , string_ ):
              random_placeholder = str(random.randrange(10000000))
          return random_placeholder
def Return__GroupWith__RegexOn__String  (group,regex,string_):
    group_setup = re.search(regex,string_)
    if group_setup == None:
      return ''
    return group_setup.group(group)
# General Tools 
def SimultaneouslyReplaceEachIn__DictOn__String ( dict_of_things_im_looking_for , text_thats_getting_changed ):
    # warinings
        # these might not work:
        # lookaheads / lookbehinds 
        # begining / end achors 
        # groups (in the replacement string) 
        # Also sometimes order may cause problems


    # if the dict is empty, don't change anything
    if len(dict_of_things_im_looking_for) == 0:
        return text_thats_getting_changed

    list_of_all_of_the_things_to_find = dict_of_things_im_looking_for.keys()
    all_of_those_things_in_order = sorted(list_of_all_of_the_things_to_find, key=lambda x: len(x))
    all_of_those_things_in_order.reverse()
    all_of_them_in_a_regex_string = "("  + "|".join(all_of_those_things_in_order) + ")" 
    
    def Is__RegexIn__String(regexstring,string): 
        # the stupid $ doesn't actually match the end 
        # at least it doesn't when there's a \n at the end 
        # so to get around this, I append (?![\s\S]) to the end
        if regexstring[-1] == '$' and regexstring[-2] != '\\':
            regexstring = regexstring + r'(?![\s\S])'
        output = re.search(regexstring,string) != None 
        return output

    def the_corrisponding_replacement(regex_found):
        string_that_was_found = regex_found.group()
        for each_item in all_of_those_things_in_order:
            # the below line could cause problems for lookahead / lookbehind / beginning / end regex 
            if Is__RegexIn__String( each_item , string_that_was_found ):
                # if an item was found, then return it's corrisponding replace value
                return dict_of_things_im_looking_for[ each_item ] 
      
        print "probably an error with Simultanious Replacement"
        print "may be due lookahead/lookbehind/beginning/end regex"
        return string_that_was_found

    return re.sub( all_of_them_in_a_regex_string , the_corrisponding_replacement , text_thats_getting_changed )



#
# defines 
#
def Fail():
    exit(0)
def ConvertToASCII_List(text):
    return [ord(each_char) for each_char in text]





Load("the_tree")
Load("All_Commands")





#
#   Globals 
#


# where all of the thinker-specifc variables are stored 
heap_ = {}
# its well.. where markers go (will be used later)
markers_ = {}

# the thinker is basically just a name, some code(as a string), and a method that executes the code
class Thinker:
    def __init__(self, name="", thinker_code=""):
        self.name         = name 
        self.thinker_code = thinker_code 

    def code_is(self, code_):
        self.thinker_code = code_ 

    def think_about(self, location_on_tree):
        global the_tree 
        exec(self.thinker_code)


# input a command instance, and this will execute it's thinker 
def think_about_func ( command_instance ):
    global All_Commands 
    global the_tree 
    # find what command template the command instance belongs to 
    if debug: print "command_instance is a: " + str(type(command_instance))
    if debug: print command_instance
    name_ = command_instance['Name']
    if debug: print "looking for: " + name_ 
    for any_command in All_Commands:
        if name_ == any_command:
            if debug: print "running the thinker: " + name_ 
            if debug: print type(any_command)
            All_Commands [ any_command ]['Thinker'].think_about( command_instance['location_on_global'] )



# fix this, create thinker maker tools 


#
#   Display thinker 
#
display_thinker = Thinker("Display")
display_thinker.code_is(r"""
if True:    
    # we have location_on_tree 
    exec( '''my_instance = the_tree'''+location_on_tree )
    contents = my_instance['Contents']
    for each_object in contents:
        think_about_func(contents[each_object])

    # any time the think_about() function is used, we need to update my_instance because the_tree has probably(hopefully) changed 
    exec( '''my_instance = the_tree'''+location_on_tree )
    contents     = my_instance['Contents']
    
    # check if all of the values are raw values
    not_all_are_raw = False 
    for each_object in contents:
        if not Is__RegexIn__String( 'Raw', contents[each_object]['Type']):
            not_all_are_raw = True 
    
    if not_all_are_raw == False:
        ascii_list   = []
        for each_object in contents:
            for each_char in contents[each_object]['ASCII_List']:
                ascii_list.append(each_char)
        my_instance['ContentType'] = 'Raw'
        my_instance['ASCII_List'] = ascii_list

    # normally there would be other stuff in here, but I'm not done 


    exec( '''the_tree'''+location_on_tree+'''= my_instance ''')
    """)
    



#
#   Text thinker 
#
text_thinker = Thinker("Text")
text_thinker.code_is(r"""
if True:
    # we have location_on_tree
    exec( '''my_instance = the_tree'''+location_on_tree )
    actual_text = my_instance['Content']

    # if it's raw text, then get the contents
    if Is__RegexIn__String( 'Raw', my_instance['Type']):
        # if it's a DoubleQuote then, convert each char to ASCII
        if Is__RegexIn__String( 'DoubleQuote', my_instance['Type']):
            my_instance['ASCII_List'] = [ord(each_char) for each_char in actual_text]

    exec( '''the_tree'''+location_on_tree+'''= my_instance ''')
    """)



#
#   Put thinkers into All_Commands 
#


All_Commands['Display_Command']['Thinker'] = display_thinker
All_Commands['Text']           ['Thinker'] = text_thinker




#
#   Think about everything
#

for each_command in the_tree:
    think_about_func(the_tree[each_command])



PrintDict( the_tree )
the_new_tree = the_tree 
Save("the_new_tree")


#
#
#   Translator 
#
#
#
#
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


Load("the_new_tree")
Load("All_Commands")
the_tree = the_new_tree 

# import from thinker
# the_tree 


#
#   Globals
#

heap = {
    'headers'    : [], 
    'namespaces' : [],
    'location'   : 0,
}

cpp_tree = {
    
}




#
#   Tools 
#

def AddHeaders             ( *strings_ ):
    global heap
    strings_list = list(strings_)
    for each_string in strings_list:
        heap['headers'].append(each_string)
def OutputHeadersCode      (           ):
    global heap 
    output_code = ''
    for each_header in heap['headers']:
        output_code = '#include <' + each_header + '>\n'
    return output_code + '\n'
def AddNamespace           ( *strings_ ):
    global heap
    strings_list = list(strings_)
    for each_string in strings_list:
        heap['namespaces'].append(each_string)
def OutputNamespace        (           ):
    global only_using_std_namespace
    if only_using_std_namespace == True:
        return 'using namespace std\n\n'
    else:
        return ''
def OutputMainFunctionCode (           ):
    global cpp_tree
    global only_using_std_namespace
    if only_using_std_namespace == True:
        main_funtion_code = '' 
        for each in cpp_tree:
            main_funtion_code = main_funtion_code +'\n' + cpp_tree[each]['code_without_namespace']
    else: 
        main_funtion_code = '' 
        for each in cpp_tree:
            main_funtion_code = main_funtion_code +'\n' + cpp_tree[each]['base_code']
    return 'int main ()\n{' + Indent(main_funtion_code) + 'return 0;\n\n} //End Of Program'
def location_on_cpp_tree   (           ):
    global heap
    return '['+str(heap['location'])+']'
def NextLocation           (           ):
    global heap 
    heap['location'] = heap['location'] + 1




class Translator:
    def __init__(self, name="", thinker_code=""):
        self.name         = name 
        self.thinker_code = thinker_code 

    def code_is(self, code_):
        self.thinker_code = code_ 

    def translate_(self, location_on_tree):
        global the_tree 
        exec(self.thinker_code)




# input a command instance, and this will execute it's translator 
def Translate ( command_instance ):
    global All_Cpp_Translators 
    global the_tree 
    # find what command template the command instance belongs to 
    if debug: print "command_instance is a: " + str(type(command_instance))
    if debug: print command_instance
    name_ = command_instance['Name']
    if debug: print "looking for: " + name_ 
    for any_command in All_Cpp_Translators:
        if name_ == any_command:
            if debug: print "running the translator: " + name_ 
            if debug: print type(any_command)
            All_Cpp_Translators [ any_command ].translate_( command_instance['location_on_global'] )
            NextLocation()




#
#   Translators
#

cpp_translators = {}

    # cpp translator output:
    #     Set base_code 
    #     Set headers 
    #     Set namespace(s)
    #     Set vars 
    #     Set traduki (compiler) vars
    #     Set global_vars 
    #     Set functions
    #     Set defines 
    #     Set preprocessor logic 




# Display translator
display_translator = Translator('Display')
display_translator.code_is(r"""
if True:
    # we have location_on_tree 
    exec( '''my_instance = the_tree'''+location_on_tree )


    arguments_list = []


    def ConvertASCII_ListToCppLiteral(ASCII_List_):
        def EscapeCharToCppString(each_char):
                if each_char ==  7: return r'\a' # alert (bell)
                if each_char ==  8: return r'\b' # backspace
                if each_char ==  9: return r'\t' # horizonal tab
                if each_char == 10: return r'\n' # newline (or line feed)
                if each_char == 11: return r'\v' # vertical tab
                if each_char == 12: return r'\f' # form feed
                if each_char == 13: return r'\r' # carriage return
                if each_char == 34: return r'\"' # quotation mark
                if each_char == 39: return r'\'' # apostrophe 
                if each_char == 63: return r'\?' # question mark 
                if each_char == 92: return r'\\' # backslash
                return chr(each_char)
        cpp_literal_ = ''
        for each in ASCII_List_:
            cpp_literal_ = cpp_literal_ + EscapeCharToCppString(each)
        return cpp_literal_
    # if there are only raw types 
    if my_instance['ContentType'] == 'Raw':
        arguments_list.append('"'+ConvertASCII_ListToCppLiteral(my_instance['ASCII_List'])+'"')
    
    # put everything into peices
    begining_                 = my_instance['Indent'] 
    command_with_namespace    = 'std::cout << ( '
    command_without_namespace = 'cout << ('
    arguments_text            = ') << ('.join(arguments_list)
    ending_                   = ') ;\n'

    # cpp translator output:
    #     Set base_code 
    #     Set headers 
    #     Set namespace(s)
    #     Set vars 
    #     Set traduki (compiler) vars
    #     Set global_vars 
    #     Set functions
    #     Set defines 
    #     Set preprocessor logic 
    AddHeaders('iostream')
    AddNamespace('std')
    exec( '''cpp_tree'''+location_on_cpp_tree()+''' = {}''' )
    exec( '''cpp_tree'''+location_on_cpp_tree()+'''['base_code']              = begining_ +command_with_namespace    +arguments_text +ending_ ''' )
    exec( '''cpp_tree'''+location_on_cpp_tree()+'''['code_without_namespace'] = begining_ +command_without_namespace +arguments_text +ending_ ''' )
    """)





#
#   Set translators 
#

All_Cpp_Translators = {
    'Display_Command' : display_translator
}





#
#   Run Translators
#


for each_command_instance in the_tree:
    Translate(the_tree[each_command_instance])





#
#   Put code together
#


# check namespaces 
if (len(heap['namespaces']) == 1) and (heap['namespaces'][0] == 'std'):
    only_using_std_namespace = True 
else:
    only_using_std_namespace = False 


output_code = ''
# preprocessor
if True:
    # headers 
    output_code = output_code + OutputHeadersCode() 
    # defines 
    # logic 
# pre main 
    # namespace
    output_code = output_code + OutputNamespace() 
    # global vars
    # function headers
# main function
output_code = output_code + OutputMainFunctionCode()

print '\n\n\n' 
print output_code 


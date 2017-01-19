
#
#
#   What is this thing for?
#
#


#
# Lets say you were creating a class (a custom variable really) 
# lets call this class a "time" variable. 
# But you don't want to have to put data into a string/number 
# Ex: time_var = "12:30" or time_var.hour(12) , time_var.minute(30)
# what you want to do is just type:
# time_var = 12:30 
# and the compiler know what you mean
# basically, you want to create your own literal/raw type 
#
# This compiler should enable that (and many more things) to happen 
# 
# But there's no way I could make an actual compiler hahaha
# so I'm going to do something more easy and compile code into a general form
# for example string/text will be compiled into ASCII or UNICODE
# then that general form will be translated into a specific language (like C++ or Python) 









#
#
#   How this thing works 
#
#

# PARSER:
# the input is source_code 
# the parser creeps over the source code character by character 
# it runs "is this command possible" code for every command, and gets values back through global vars 
#       inside of that code, commands can look for other commands even if the parent command 
#       doesn't know what the child command looks like 
# the parser then finds the command that says it recognizes the largest amount of characters 
# (this part (above) is actually going to change in the next version, its #1 on my coding todo list) 
# and the parser then runs that command's "execute code"
#       the command when executed puts all of it's info into a global variable called the_tree (it's a dictionary of dictionaries)
#       things like command instance #/ command name / command contents are all stored in the_tree
#       the command can also parse other commands inside it and have them put their contents into a subsection of the_tree
# then once all the commands have been parsed, the_tree is handed off to the thinker.py 

# THINKER:
# the thinker's main job is that, 
# it allows commands to do more complex logic without slowing down parse time 
#       so lets say you have a string "help im stuck in a computer"
#       we want to turn that string into ASCII, 
#       so once the thinker gets the_tree 
#       it goes over all the command_instances on the tree  
#       and if it finds a string/text command_instance 
#       it looks for the "contents" section and then converts the contents into ASCII
# once it's done with all of it's logic the thinker passes the_new_tree to the translator 

# TRANSLATOR:
# translators are language specific, so there isn't one general "the translator" file 
# they take the_tree/the_new_tree and convert it into a specific language 
# so for example if the C++ translator sees the "Display" function 
# it will know to:
#     use "cout <<"
#     include the "iostream" header  
#     end the command with a ";"
#     etc  
# and the rest of the C++ translator would do things like add the main () function 

















#ToDo:
    # redo parse_function 
    # Make parser object oriented 
    # Add *NEWLINE* and other escaped characters 
    # Add Code vars 
    

















#/////////////////////////////////////////////
#
#     Initial Setup   
#
#/////////////////////////////////////////////

    #------------------------------------------------
    # Import Python Tools
    #------------------------------------------------
    
import pdb          # debugging 
import random
import sys
import os
import regex as re
import itertools
import datetime
import pickle 

    #------------------------------------------------
    # Load Source File
    #------------------------------------------------
    

# The below code will be un-commented once 
# this compiler is running on files instead of just a literal string 
#      # get the target file location from the middle man file 
#      middleman_file          = open('/Users/Jeff/Library/Application Support/Sublime Text 3/Packages/User/AlphaFilePath.txt' ,'r+')
#      location_of_target_file = middleman_file.read()
#      middleman_file.close()
#      # get the target file and put it in a string source_ 
#      targetfile              = open(  ('%s' % ( (re.search('(.+)$' , location_of_target_file)) ))   ,'r+')
#      source_                 = targetfile.read()
#      targetfile.close()
#      # make copies of source
#      source_copy             = source_ 
#      the_copy_lines          = source_copy.splitlines()


# This is what is going to be parsed
source_copy = '''
Display "Hello World" " its me " "blah blah blah"
'''



    #------------------------------------------------
    # Set Flags 
    #------------------------------------------------
    
# settings
debug     = True







# 
# Set Defs  
#



# redefines
    # I basically just rename/simplify things 
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
    # this is actually a really nice tool that I'm suprised Python 
        # doesn't implement itself 
        # most of it is code from online that I found and
        # modified into working my way 
        # if you want to do something like 
        # replace all current A's with B's and all current B's with A's 
        # this is basically the only surefire way you can do it

    # warinings
        # these probably won't work:
        # lookaheads / lookbehinds 
        # begining / end achors 
        # groups (in the replacement string) 
        # Also sometimes order may cause problems


    # if the dict is empty, don't change anything
    if len(dict_of_things_im_looking_for) == 0:
        return text_thats_getting_changed

    list_of_all_of_the_things_to_find = dict_of_things_im_looking_for.keys()
    all_of_those_things_in_order      = sorted(list_of_all_of_the_things_to_find, key=lambda x: len(x))
    all_of_those_things_in_order.reverse()
    all_of_them_in_a_regex_string     = "("  + "|".join(all_of_those_things_in_order) + ")" 
    
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
























#/////////////////////////////////////////////
#
#     Global Stuff 
#
#/////////////////////////////////////////////


# general things that happen 
    # newlines are added to the begining and end of the source 
    # a standard command (when found) should remove everything before it, but not spaces/newlines after it


# missing features 
    # Code vars 
    # code functions 


# need fixing:
    # what happens if two commands tie 
    # how a command can find the end / begining of the file 


#Global vars 
if True: 
    IHaveNotBeenRuledOut = False
    IHaveBeenRuledOut    = True
    ICanStart            = False
    Fail                 = False
    IEndAt               = 0
    COUNTER              = 0
    All_Commands         = {}
    code_                = ''
    the_tree             = {}
    local_tree           = {}
    most_globals = '''
    global IHaveBeenRuledOut
    global IHaveNotBeenRuledOut 
    global ICanStart            
    global IEndAt               
    global COUNTER              
    global All_Commands    
    global the_tree   
    '''









#/////////////////////////////////////////////
#
#     Parse Def's 
#
#/////////////////////////////////////////////



# tools 
def for_each_command_with__do__      (dict_attributes_text , Code):
    # input: attribute
    # output: Code  
    Code = '''\nfor each_command in All_Commands:
    #if debug: print "okay I'm checking: " +  each_command 
    #if debug: print """for the '''+dict_attributes_text+''' attribute(s)""" 
    if exists(All_Commands[ each_command ] , """'''+dict_attributes_text+'''""" ): 
        '''+Indent(Indent(Code))
    return Code
def convert_attributes_tuple         (attributes_tuple):
    attributes_list = list(attributes_tuple)
    return '["'+'"]["'.join(attributes_list)+'"]'
def all_commands_with                (*attributes):
    # input: texts
    # output: list_of_commands     
    list_of_commands = []
    exec(
        for_each_command_with__do__(
            convert_attributes_tuple(attributes) , 
            'list_of_commands.append(All_Commands[ each_command ])' 
                                    )
        )
    return list_of_commands
def values_of_commands_with          (*attributes):
    # input: texts
    # output: list_of_values
    list_of_values = [] 
    exec( for_each_command_with__do__( 
                convert_attributes_tuple(attributes),  
                '''list_of_values.append(All_Commands[ each_command ]'''+convert_attributes_tuple(attributes)+''') '''
        )                             ) 
    return list_of_values 
def all_scouts_with                  ( attribute ):
    # input  = text
    # output =  [ [ command_name , scout_name ] , [ command_name , scout_name ] , etc   ] 
    
    # find the scout lister for the attribute
    attribute_text = '''["Scout_lister"]["'''+attribute+'''"]'''
    list_of_all_scouts = []
    # get the list 
    exec( for_each_command_with__do__( 
    attribute_text,
    '''\nscouts_list = All_Commands[ each_command ]'''+attribute_text+'''\nfor each_scout in scouts_list:
    command_name = each_command
    scout_name   = each_scout 
    list_of_all_scouts.append([ command_name , scout_name ]) ''' ))
    #return the list of scouts
    return list_of_all_scouts 
def UniqueID                         ():
    global COUNTER 
    COUNTER = COUNTER + 1 
    return str(COUNTER)
def NumberOfCommandsSoFar            ():
    global COUNTER 
    return COUNTER 
def parse_function                   ( code_ , list_of_scouts , location_on_global):
    # code is text, it's the WHOLE code that needs to get parsed
    # list_of_scouts = [ [ command_name , scout_name ] , [ command_name , scout_name ]     ]
    # the_tree = {}              
    global IHaveBeenRuledOut
    global IHaveNotBeenRuledOut 
    global ICanStart            
    global IEndAt               
    global COUNTER              
    global All_Commands   
    global the_tree   
    global Fail   


    # load the scouts from the command tree
    Scouts_                = [] #   [   { 'is_possible_Code' : *CODE* , 'when_executed' : *CODE* , 'Name' : *text* } , { 'is_possible_Code' : *CODE* , 'when_executed' : *CODE* , 'Name' : *text* } , etc  ] 
    for each_scout in list_of_scouts:
        command_name = each_scout[0]
        scout_name   = each_scout[1]
        if debug: print "added scout :" + scout_name
        if debug: print "from command:" + command_name
        Scouts_.append(All_Commands[ command_name ]['Scouts_'][ scout_name ])


    at_least_one_scout_has_been_set = False
    biggest_confirmed_length        = 0
    attempted_length                = 1 
    scout_to_deploy                 = {}
    current_scout                   = Scouts_.pop()
    
    while True:
            # reset stuff
            ICanStart            = False 
            IHaveNotBeenRuledOut = False 
            IHaveBeenRuledOut    = True
            code_snippet         = code_[ 0:attempted_length ]
            #debugging
            if debug: print "testing scout:" + current_scout['Name']
            if debug: print "on code:"      + code_snippet


            exec(current_scout['is_possible_Code']) 



            # debug
            if debug: print "okay after running: "    + current_scout['Name']
            if debug: print "    IHaveBeenRuledOut: " + str(IHaveBeenRuledOut)
            if debug: print "    ICanStart: "         + str(ICanStart) 
            if debug: print "    IEndAt: "            + str(IEndAt) 






            # if the scout can start, record the value
            if ICanStart == True:
                    if debug:  print "new max set:" + current_scout['Name']
                    scout_to_deploy                 = current_scout 
                    at_least_one_scout_has_been_set = True 
                    biggest_confirmed_length        = attempted_length
                    attempted_length                = attempted_length + 1 
                    
                    #import remaining_code
                    #import unconfirmed_tree


            # if scout is ruled out, see if there's another scout, 
            # if there's another scout then reset the length and go to the next scout
            if IHaveNotBeenRuledOut == False:
                    if debug: print "this scout has been ruled out"
                    if len(Scouts_) > 0:      attempted_length = biggest_confirmed_length ; current_scout = Scouts_.pop()
                    else: break

            
            # if there are no more characters to add, then execute the command
            elif len(code_) <= attempted_length: 
                    break
            # if a scout is possible, add a character and try again 
            else: 
                    attempted_length = attempted_length + 1 


    # fail check and debugging
    if not at_least_one_scout_has_been_set: print ":/ no scouts found anything" ; Fail = True ; return '' 
    else                                  : Fail = False 
    if debug                              : print "okay deploying scout: " + scout_to_deploy ['Name']


    # setup the code_snippet 
    # let the scout change the code_ and the the_tree 
    print scout_to_deploy['execute_Code']
    exec( scout_to_deploy['execute_Code']) 
    return code_ 













#/////////////////////////////////////////////
#
#    Scout writer
#
#/////////////////////////////////////////////
# scouts are the things that commands have that 
# do both finding/executing the command 
# they are just a term I made up to help think about the problem


# abbreviations  
def cascade              (list_):
    if len(list_) == 1:
        output_ = list_ 
    else:
        buildup = ""
        output_ = []
        for each_item in list_:
            buildup = buildup + each_item 
            output_.append(buildup)
        output_.reverse()
    return r'(' + ( '|'.join(output_) ) + r')'
def splice_colons        (regex):
    return re.split(r'(?<!\\\\):',regex)
def nothing_left         ():
    return '''len(local_code) ==            0          '''
def something_left       ():
    return ''' not '''+nothing_left()
def something_was_changed():
    return '''len(local_code) != len(local_code_before)'''
def no_change            ():
    return '''len(local_code) == len(local_code_before)'''
def set_local_code_before():
    return '''\n    local_code_before = local_code \n'''
def big_comment          (comment):
    return '''
    ####################################
    ###     '''+comment+'''
    ####################################
    '''
def normal_comment       (comment):
    return '''
    ###     '''+comment+'''
    '''
def finder_              ( is_possible_Code , execute_Code , decider_Code ):
    return {
    'is_possible_Code'   : is_possible_Code,
    'execute_Code'       : execute_Code,
    'decider_Code'       : decider_Code
    }
then_           = ''': '''
not_possible    = '''IHaveBeenRuledOut = True  ; IHaveNotBeenRuledOut = False ; IEndAt =                      0                     ;                   break'''
possible_       = '''IHaveBeenRuledOut = False ; IHaveNotBeenRuledOut = True  ; IEndAt =               len(code_snippet)            ;                   break'''
can_start_whole = '''IHaveBeenRuledOut = False ; IHaveNotBeenRuledOut = True  ; IEndAt =               len(code_snippet)            ; ICanStart = True; break'''
can_start_part  = '''IHaveBeenRuledOut = False ; IHaveNotBeenRuledOut = True  ; IEndAt = len(code_snippet) - len(local_code_before) ; ICanStart = True; break'''
# slicers
#       scouts use slicers for the "is_possible" part of a command
#       slicers are another thing I made up that basically remove a peice of code from the begining of a string 
#       typically they are either a regular expression or a command 
def remove_command       ( code_ , list_of_scouts , location_on_global , original_snippet):

    global IHaveBeenRuledOut
    global IHaveNotBeenRuledOut 
    global ICanStart            
    global IEndAt               
    global COUNTER              
    global All_Commands                             
    

    # load the scouts from the command tree
    Scouts_                = [] #   [   { 'is_possible_Code' : *CODE* , 'when_executed' : *CODE* , 'Name' : *text* } , { 'is_possible_Code' : *CODE* , 'when_executed' : *CODE* , 'Name' : *text* } , etc  ] 
    for each_scout in list_of_scouts:
            command_name = each_scout[0]
            scout_name   = each_scout[1]
            if debug: print "added scout :" + scout_name
            if debug: print "from command:" + command_name
            Scouts_.append(All_Commands[ command_name ]['Scouts_'][ scout_name ])


    code_snippet     = code_ 
    counter_         = -1
    first_try        = True
    while True:
        counter_     = counter_ + 1 
        code_snippet = code_[   0  :  ( len(code_) - counter_ )   ]
        

        for each_scout in Scouts_:
                
                # reset stuff
                ICanStart            = False 
                IHaveNotBeenRuledOut = False 
                IHaveBeenRuledOut    = True
                IEndAt               = -1
                # debug 
                if debug: print 'len(Scouts_)'
                if debug: print len(Scouts_)
                if debug: print "okay I'm testing for: "          + each_scout['Name']
                if debug: print 'this is the input code_snippet:' + code_snippet 
                if debug: print 'location_on_global' 
                if debug: print location_on_global 




                exec(each_scout['is_possible_Code'])  
                



                # debug
                if debug: print "okay after running: "    + each_scout['Name']
                if debug: print "    IHaveBeenRuledOut: " + str(IHaveBeenRuledOut)
                if debug: print "    ICanStart: "         + str(ICanStart) 
                if debug: print "    IEndAt: "            + str(IEndAt) 




                # if the scout can start
                if   ICanStart == True:
                        # debug
                        if debug: print "therefor, I can start"


                        output_      = code_   [ IEndAt :  len(code_) ] # whatever is leftover 
                        code_snippet = original_snippet                 # this is just restoring the snippet 
                        # fix this, when code_snippet is short 
                        ICanStart            = False # these are here to reset the globals before going back out 
                        IHaveNotBeenRuledOut = False 
                        IHaveBeenRuledOut    = True
                        return output_

                
                # if the scout can't start, but it is possible on the first try
                elif (IHaveNotBeenRuledOut == True) and (first_try):
                        # debug 
                        if debug: print "therefor, I haven't been ruled out"
                        if debug: print "IEndAt:" + str(IEndAt)


                        output_       = code_  [ IEndAt : len(code_) ] #whatever is leftover 
                        code_snippet  = original_snippet               # this is just restoring the snippet 
                        ICanStart            = False # these are here to reset the globals before going back out 
                        IHaveNotBeenRuledOut = False 
                        IHaveBeenRuledOut    = True
                        return output_

               
                # if the scout has been ruled out, go to the next scout 
                elif IHaveNotBeenRuledOut == False:
                        if debug: print "therefor, I have been ruled out"
                        pass
                

                # if no scouts could be found, shortent the snippet and try again 
                # if the snippet is only 1 char long, then rule out the scout
        if len(code_snippet) <= 1:
                        code_snippet = original_snippet # this is just restoring the snippet 
                        ICanStart            = False # these are here to reset the globals before going back out 
                        IHaveNotBeenRuledOut = False 
                        IHaveBeenRuledOut    = True
                        return code_ 

        first_try = False 
def hidden_slice_regex   ( regex ):
    a_list_ = splice_colons(regex)
    return normal_comment('Hidden Regex Slice')+ Indent('\nif debug: print "doing hidden regex slice"\n'+r"""local_code = re.sub(r'(^"""+''.join(a_list_)+r"""|^"""+cascade(a_list_)+r"""$(?![\s\S]))','',local_code )"""+'\n')
def slice_regex          ( regex ):
    return big_comment('Regex Slice') + Indent('\nif debug: print "okay In doing a regex slice using:" + r"""\'\'\''+regex+"'''\"\"\"") + set_local_code_before() + hidden_slice_regex(regex)
def slice_command        ( code_that_sets_scouts_list ):
    return Indent('\n'+code_that_sets_scouts_list) + set_local_code_before()+  Indent('''\nlocal_code = remove_command( local_code , scouts_list , location_on_global ,  code_snippet )\n''')
def loop_slice           ( finder_chain ):
    slicer_code  = []
    for each_finder in Range_(finder_chain):
        dict_ = finder_chain[each_finder]
        slicer_code.append(dict_[ 'is_possible_Code' ])
    slicer_code.append(inbetween_check)

    the_internal_code           = Join(slicer_code)
    protected_local_code_before = 'protected_local_code_before' + ReturnRandomNumberStringThatsNotIn__(the_internal_code)
    protected_local_code        = 'protected_local_code'        + ReturnRandomNumberStringThatsNotIn__(the_internal_code)
    return '''
    '''+protected_local_code_before + '''= local_code
    while True:
        '''+protected_local_code+''' = local_code
        '''+Indent(the_internal_code)+'''
    if (IHaveBeenRuledOut == True) and '''+something_left()+then_+'''
        local_code        = ''' + protected_local_code        + '''
        local_code_before = ''' + protected_local_code_before + '''
    '''
# execution tools
#       these are like slicers, but are used for the execution of the code
#       the main difference is that the don't worry about partial matches and
#       they often put their match into a variable inside of the_tree
def extract_command      ( code_that_sets_scouts_list ,  internal_name='' ):
    # if there's a name
    if internal_name != '':
        return '''
        '''+Indent(code_that_sets_scouts_list)+"""
    internal_location_on_global = location_on_global+'''['"""+internal_name+"""']'''
    if debug: print 'location_on_global before extract_command with a name' 
    if debug: print location_on_global 
    exec('''global the_tree\nthe_tree'''+internal_location_on_global+''' = {}''')
    code_ = parse_function( code_ , scouts_list , internal_location_on_global)
    """
    # if there isn't a name
    else:
        return '''
        '''+Indent(code_that_sets_scouts_list)+"""
    if debug: print 'location_on_global right before extracting a command' 
    if debug: print location_on_global 
    code_ = parse_function( code_ , scouts_list , location_on_global)
        """
def execute_remove_regex (        regex_input         ,  internal_name='' ):
    regex_list = splice_colons(regex_input)
    regex = ''.join(regex_list)
    if internal_name == '':
        return """
    code_ = re.sub("""+r"""r'^"""+regex+'''', '' , code_ )
    '''
    else:
        if debug: print 'internal_name' 
        if debug: print internal_name 
        return """
    the_value = Return__GroupWith__RegexOn__String( 0 ,"""+r"r'^"+regex+"""' , code_ )
    exec('''the_tree'''+location_on_global+'''['"""+internal_name+"""'] = the_value''')
    code_ = re.sub("""+r"""r'^"""+regex+'''', '' , code_ )
    ''' 
def extract_loop         (           name             ,  finder_chain     ):
    executer_code  = []
    for each_finder in Range_(finder_chain):
        dict_ = finder_chain [ each_finder ]
        executer_code.append(dict_[ 'execute_Code' ])

    the_internal_code           = Join(executer_code)

    protected_counter            = 'counter_'                     + ReturnRandomNumberStringThatsNotIn__(the_internal_code)
    protected_code_before        = 'protected_code_before'        + ReturnRandomNumberStringThatsNotIn__(the_internal_code)
    protected_location_on_global = 'protected_location_on_global' + ReturnRandomNumberStringThatsNotIn__(the_internal_code)
    
    # could prob make a func in here and use that to avoid needinng the protected vars
    return '''
    # start loop 
    '''+ protected_counter           +''' = 0
    '''+ protected_location_on_global+''' = location_on_global
    location_on_global = location_on_global + """["'''+name+'''"]"""
    if debug: print 'location_on_global before loop command with a name' 
    if debug: print location_on_global 
    exec("""global the_tree\nthe_tree"""+location_on_global+""" = {}""")
    while (True):
        '''+ protected_counter +''' = '''+ protected_counter +''' + 1
        # start adding objects 
        # add "object" + loop_number to local 
        '''+protected_code_before    +''' = code_
        '''+Indent('\n'+the_internal_code)+'''
        # this will remove the object from the remaining_code 
        # if no more objects, exit loop 
        if '''+protected_code_before+''' == code_: break 
    # name the tree within the the_tree 
    location_on_global = '''+ protected_location_on_global +'''
    '''
# deciders (inbetween/after slicers)
#       these normally go after slicers
#       they decide whether or not a command can start 
inbetween_check     = big_comment('Decider: inbetween_check'    )+'''
    if   '''+nothing_left()+then_ + possible_   +'''
    elif '''+no_change()+   then_ + not_possible+'''
    '''
end_check           = big_comment('Decider: end_check'          )+'''
    if    '''+nothing_left()+then_+can_start_whole+'''
    else                                                                                         '''+then_+not_possible+'''
    '''
end_check_lookahead = big_comment('Decider: end_check_lookahead')+'''
    if    '''+nothing_left()+' and '+something_was_changed()+then_+can_start_part+'''
    elif  len(local_code_before) == 0                                                            '''+then_ + possible_ + '''
    else                                                                                         '''+then_ + not_possible + '''
    '''
# finders
#       finders are 1 layer below scouts 
#       they combine slicers/deciders/execution tools 
def remove_regex    (                                   regex_      ):
    return finder_ ( slice_regex ( regex_ ) , execute_remove_regex( regex_ ) , '' )
def lookahead_regex (                                   regex_      ):
    return finder_ ( slice_regex ( regex_ ) , execute_remove_regex( regex_ ) , 'Custom:'+end_check_lookahead )
def regex_          (           regex_           , internal_name='' ):
    if internal_name == '':
        return finder_ ( 
                    slice_regex         ( regex_ ) , 
                    execute_remove_regex( regex_ ) , 
                    inbetween_check 
                        )
    else:
        return finder_ ( 
                    slice_regex         ( regex_                 ) , 
                    execute_remove_regex( regex_ , internal_name ) , 
                    inbetween_check 
                        )
def command_        ( code_that_sets_scouts_list , internal_name='' ):
    return finder_ ( 
        slice_command   (  code_that_sets_scouts_list ,               ) , 
        extract_command (  code_that_sets_scouts_list , internal_name ) , 
        inbetween_check 
                   )
def loop_           (       internal_name        , *finders_tuple   ):
    finders_ = list(finders_tuple)
    return finder_ ( 
            loop_slice   (                finders_ ) , 
            extract_loop ( internal_name, finders_ ) , 
            inbetween_check 
                   )
# super tool
#       writing a scout by hand is extremely tedious and has lots of memorization 
#       I created a find() tool to try and make it easier, however there are many more
#       features that still need to be added and much refinement that needs to be done
#       before it is easy enough that other people can write scouts without a lot of pain
# To get an idea of how the find() command works, just read the scouts below
def find( *finders_tuple):
    # name , type , finders_
    finders_ = list(finders_tuple)

    global standard_fail_check_Code
    global standard_lookahead_fail_check_Code
    global standard_end_fail_check_Code
    
    # this allows attributes of the higher command to also be added to the tree's of lower commands
    # fix this, in later versions allow carryover to be set by input, and allow certain attributes to carryover
    attributes_dont_carryover = True

    is_possible_output   = [] 
    when_executed_output = []   
    
    custom_decider_regex = r'^Custom:'         
    attribute_regex      = r'(\w+):(.+)'
    
    attributes_ = ''
    scout_name  = ''
    #each_item = 0
    
    if Is__RegexIn__String( r'^CommandName:(\w+)$' , finders_[0]):
        scout_name = Return__GroupWith__RegexOn__String(2, attribute_regex, finders_[0]) 
        finders_.pop(0)
    else:
        print "hey all the finders need names, \njust use CommandName:*theactualname* in the first arugment"
        exit(0)

    finders_2 = []
    for each_finder in finders_: 
        #each_item = each_item + 1 
        if type(each_finder) == str:
            if Is__RegexIn__String(attribute_regex , each_finder):
                finder_attribute       = Return__GroupWith__RegexOn__String(1, attribute_regex, each_finder)
                finder_attribute_value = Return__GroupWith__RegexOn__String(2, attribute_regex, each_finder) 
                attributes_            = attributes_ + Indent( '\n' + '''exec("""the_tree"""+location_on_global+"""[ \''''+finder_attribute+'''' ] = '''+"'"+finder_attribute_value+"'\"\"\")")
        else:
            finders_2.append(each_finder)
    
    finders_ = finders_2
    

   
    
    # for all the arguments given
    for each_item in Range_(finders_):
        dict_ = finders_[each_item]
        is_possible_output.append   (   dict_['is_possible_Code'] ) 
        is_possible_output.append   (   dict_['decider_Code']     ) 
        when_executed_output.append (   dict_['execute_Code']     ) 
        when_executed_output.append (   Indent('''\nfor each_attribute in local_tree:\n    the_tree [ \''''+scout_name+'''' ][ each_attribute ] = local_tree[ each_attribute ]\nlocal_tree = {} ''')     ) 
    
    
    # replace the last decider with an end_check
    if  Is__RegexIn__String( custom_decider_regex , is_possible_output[-1]): is_possible_output[-1] = re.sub( custom_decider_regex , '' , is_possible_output[-1] )
    else                                                                   : is_possible_output[-1] = end_check 

    is_possible_part = '''\nwhile True:  # this is so it can be indented and so it can be broken out of 
    '''+most_globals+'''
    local_code = code_snippet
    '''+ Join(is_possible_output) + '''\n    break \n'''
    
    execute_part = '''\nif True:  # this is so it can be indented
    '''+most_globals+"""
    command_counter = UniqueID()
    location_on_global = location_on_global + '''[ '"""+scout_name+"""'''+command_counter+'''' ]'''
    exec( '''the_tree'''+location_on_global + ''' = {}''' )
    """+attributes_+"""
    exec( '''the_tree'''+location_on_global+ '''['Counter'           ] = command_counter''' )
    exec( '''the_tree'''+location_on_global+ '''['location_on_global'] = location_on_global''' )
    """+ Join(when_executed_output) 

    return { 
           'Name'               : scout_name,
           'is_possible_Code'   : is_possible_part,
           'execute_Code'       : execute_part
           }


# problems:
    # what about more complex finding logic 
    # what about a loop with a lookahead at the end of it 
    # how to add multiple finders for the same scout/command 


# Right now there are only 3 sad commands, Display, Sort (which doesn't sort), and Text 

display_scout =  find( 
            "CommandName:Display_Command"   ,
            "Name:Display_Command"                  ,
            "Type:Command"                  ,
            regex_  (r'\n *' , 'Indent'   ) , 
            regex_  (r'D:i:s:p:l:a:y'     ) , 
            loop_   ( 
                      "Contents"                  ,
                      command_ ( '''\nscouts_list = all_scouts_with('can_be_displayed')''' ) 
                    )                       ,
            remove_regex    (r' +'),
            lookahead_regex (r'\n') 
                     )

sort_scout =  find( 
            "CommandName:Sort_Command"         ,
            "Name:Sort_Command"                ,
            "Type:Command"                     ,
            regex_   (r'\n *'     , 'Indent' ) , 
            regex_   (r'S:o:r:t'             ) , 
            command_ ( '''\nscouts_list = all_scouts_with('can_be_sorted')''' , 'Argument'),
            remove_regex    (r' +')            ,
            lookahead_regex (r'\n')            ,
                  )


text_DoubleQuoteRaw_Scout =  find( 
            "CommandName:Text"                ,
            "Name:Text"                       ,
            "Type:ObjectRawDoubleQuote"       ,
            "DisplayType:in_line"             ,
            regex_  (r' +:"')                 , 
            regex_  (r'[^\n\"]+', 'Content')  , 
            regex_  (r'"')                    ,
                                  )




#/////////////////////////////////////////////
#
#     Commands
#
#/////////////////////////////////////////////
# this is where commands are put together 
# one day this will likely happen outside of this file 




All_Commands[ 'Display_Command' ] = \
    {
    
    "Scout_lister"  : \
                    { 'open_code'        : [ 'non_option_Scout' ], } , 

    'Scouts_'       : \
                    { 'non_option_Scout' : display_scout         , } ,

    'Thinker'       : '''if True:

    '''

    } # End Display Command 



All_Commands[ 'Text' ] = \
    {
    
    "Scout_lister"  : \
                    { 'can_be_displayed' : [ 'double_quote_raw' ]    ,
                      'can_be_sorted'    : [ 'double_quote_raw' ]    , } , 

    'Scouts_'       : \
                    { 'double_quote_raw' : text_DoubleQuoteRaw_Scout , } ,

    } # End Text Command 




All_Commands[ 'Sort_Command' ] = \
    {
    
    "Scout_lister"  : \
                    { 'open_code' : [ 'main' ]  , } , 

    'Scouts_'       : \
                    { 'main'      : sort_scout  , } ,

    } # End Text Command 






#/////////////////////////////////////////////
#
#     Execution 
#
#/////////////////////////////////////////////
# the parse_function only parses 1 command 
# so it has to be put in a loop to parse the whole source_code 


code_           = source_copy 
another_counter = 0 
starting_point  = ''
while(True):
    another_counter = another_counter + 1 
    if another_counter > 400: 
        print "inf loop 422349023"
        break 
    code_ = parse_function( code_ , all_scouts_with('open_code') , starting_point )

    print "this is the code"
    print code_ 
    # if there's nothing but whitespace remaining, then the end of the file has been found 
    if (not Is__RegexIn__String( r'^([\n \t]*)$' , code_ )) and Fail == True:
        print "well somewhere there was code where no command could be found :/"
    if Is__RegexIn__String( r'^([\n \t]*)$' , code_ ):
        print "end of file found" 
        break 


print 'Full Code Tree\n\n'
PrintDict(the_tree)
Save("the_tree")
Save("All_Commands")




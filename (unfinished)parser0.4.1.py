# things to work on 
    # clean up the recursive finders 
    # maybe make CODE global for runtime efficieincy
    # make a more efficient method for finder switch resetting
    # update to python 3 and make FIRST a nonlocal var 
        # after fixing that, make InternalParse use FIRST for optimazation  










import pdb          # debugging 
import random
import sys
import os
import regex as re
import itertools
import datetime
import pickle 
from math import *


def test(varname_string):
    print varname_string
    exec ('print '+ varname_string)
    exit(0) 
def Is__RegexIn__String  (regexstring,string): 
    # the stupid $ doesn't actually match the end 
    # at least it doesn't when there's a \n at the end 
    # so to get around this, I append (?![\s\S]) to the end
    if regexstring[-1] == '$' and regexstring[-2] != '\\':
        regexstring = regexstring + r'(?![\s\S])'
    output = re.search(regexstring,string) != None 
    return output
def LocationOf__RegexStartIn__String    (regex,string):
  group_setup = re.search(regex,string)
  return group_setup.start()
def LocationOf__RegexEndIn__String      (regex,string):
  group_setup = re.search(regex,string)
  return group_setup.end()
def Return__GroupWith__RegexOn__String  (group,regex,string_):
    group_setup = re.search(regex,string_)
    if group_setup == None:
      return ''
    return group_setup.group(group)
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
    return output_
def ReplaceQuotes(input_regex_string):
    first_quote = r'(?<!\\)"'
    second_quote = r'([A-Za-z0-9\._ ]+)"'
    if Is__RegexIn__String(first_quote+second_quote, input_regex_string):
        group_setup     = re.search( first_quote+second_quote , input_regex_string )
        return input_regex_string[  0 : group_setup.start() ] + '(' + '|'.join(cascade(list(group_setup.group(1)))) + ')' + input_regex_string[  group_setup.end() : len(input_regex_string)  ]
        # same thing as above broken down
        #content_        = group_setup.group(1)
        #content_as_list = list(content_)
        #cascade_        = cascade(content_as_list)
        #replacement_    = '(' + '|'.join(cascade_) + ')'
    else:
        return input_regex_string      
def RegexFinder( input_name , input_regex ):
    new_string = ''
    while True:
        new_string = ReplaceQuotes(input_regex)
        if new_string == input_regex:
            break
        input_regex = new_string
    return input_regex
def Indent   (input_, indent_='    '):
    if type(input_) == str:
        if not Is__RegexIn__String(r'^ *\n',input_):
            input_ = indent_ + input_ 
        return re.sub('\n','\n'+indent_ , input_) 
    elif type(input_) == list:
        for each_item in Range_(input_):
            input_[each_item] = re.sub('\n','\n'+indent_, input_[each_item]) 
        return input_ 
def UnIndent (input_,indent_='    '):
    if type(input_) == str:
        input_ = re.sub(r'^'+indent_, '' ,input_)
        return re.sub('\n'+indent_,'\n' , input_) 
    elif type(input_) == list:
        for each_item in Range_(input_):
            input_[each_item] = re.sub(r'^'+indent_, ''  , input_[each_item])
            input_[each_item] = re.sub('\n'+indent_,'\n' , input_[each_item])
        return input_ 

# import code 
CODE = ''
All_Commands = set()
All_Scouts   = set()
All_Finders  = set()







#
#
#
# Class Creation 
#
#
#


class Command: 
    global All_Commands
    def __init__(self, input_name , input_scouts=[]):
        All_Commands.add(self)
        self.name   = input_name
        self.scouts = input_scouts

    def AddScout(self, scout):
        self.scouts.append(scout)

    def ScoutsFor(self, attribute):
        list_of_scouts_with_attribute = []
        for each_scout in self.scouts:
            if attribute in each_scout.attributes:
                list_of_scouts_with_attribute.append(each_scout)
        return list_of_scouts_with_attribute 

Display = Command('Display')






class Scout:
    global CODE
    global All_Scouts
    def __init__(self, input_name):
        # permanent 
        All_Scouts.add(self)
        self.name        = input_name 
        self.attributes  = []
        self.finder      = None
        self.thinker     = None 
        # this needs to add the thinker to TreeData
        self.deploy_code = 'TreeData[\'Thinker\'] = self.thinker'
        # reset after search 
        self.memory      = {}



    def AddAttribute(self,attribute):
        self.attributes.append(attribute)

    def SetFinders(self , FindersList):
        self.finder = FindersList 

    def Has(self,attribute):
        if attribute in self.attributes: 
            return True 
        else:
            return False 



    def ClearFinderData(self):
        self.finder.ResetSwitch()

    def ClearMemory(self):
        self.memory = {}

    def Reset(self):
        self.ClearMemory 
        self.ClearFinderData


    '''
    Scout finder chain should have an evaulation finder as it's last finder 
    # the evaluation finder should take all the data and decide whether or not the correct 
    stuff has been found 
    '''
    
    def Test(self, input_START ,  input_DATA={} ,  input_CODE=CODE ):
        # check me, make sure my inputs are correct
        return self.finder.SearchResults(input_START, input_DATA, input_CODE)

    
    def Deploy(self):
        # check me, see how finders return TreeData
        FinderResults = self.memory
        RestartAt     = self.memory['RestartAt']
        TreeData      = self.memory['TreeData' ]
        exec(self.deploy_code) 
        return { 
                'RestartAt' : RestartAt ,  
                'TreeData'  : TreeData  , 
               }

display_open_code = Scout('display_open_code')
display_open_code.AddAttribute('open code')
Display.AddScout(display_open_code)




class Finder:
    global CODE 
    global All_Finders
    def __init__(self,input_name='',input_code=''):
        # should never be cleared
        All_Finders.add(self)
        self.name         = input_name 
        self.code         = input_code 
        # will be cleared once for every MainParse 
        self.switch_value = None 
        self.semi_static_vars = {}   


    def help(self):
        print "Finders are used by Scouts (see Scout.help) to... find... things"
        '''Finder Code format
        Key vars: 
            START, 
            CODE 
            DATA
        use: 
            InternalFind(name_of_finder, input_START , input_CODE, input_DATA)
        set: 
            FinderSwitchValue , 
            FinderStart, 
            FinderEnd, 
            FinderSwapCode
            FinderData
            FinderRestartLocation
        '''

        exit(0)

    def SetSwitchValue(self,input_switch_value):
        self.switch_value = input_switch_value


    # fix this, add this to help()
    def ResetLocalStatics(self):
        self.semi_static_vars = {}   
        self.semi_static_vars ['START']         = 0 
        self.semi_static_vars ['END'  ]         = 0
        self.semi_static_vars ['DATA' ]         = {}
        self.semi_static_vars ['RESTART' ]      = 0
        self.semi_static_vars ['TREEDATA']      = {}
        self.semi_static_vars ['SWITCH_VALUE' ] = None 

    # fix this, add this to help()
    def ResetSwitch(self):
        self.switch_value     = None
        self.ResetLocalStatics()

    def SetCode(self, input_code):
        # has access to the vars: START, CODE, DATA, RESTART
        # needs to return several values
        # { 
        #     'Found'    : FinderSwitchValue ,
        #     'Start'    : FinderStart, 
        #     'End'      : FinderEnd, 
        #     'Data'     : FinderData, 
        #     'RestartAt': FinderRestartLocation 
        #     'TreeData' : TreeData
        # }
        self.code = input_code 



    # fix this, add details to help 
    def SearchResults(self, input_START, input_CODE=CODE, input_DATA={}):
        global CODE
        if (FIRST == True) and (self.switch_value != None):
                FIRST = False 
                
                if self.switch_value == False:
                    return { 'Found' : False }
                else:
                    # { 
                    #     'Found'    : FinderSwitchValue ,
                    #     'Start'    : FinderStart, 
                    #     'End'      : FinderEnd, 
                    #     'Data'     : FinderData, 
                    #     'RestartAt': FinderRestartLocation 
                    #     'TreeData' : TreeData
                    # }
                    return  { 
                            'Found'    : self.switch_value                 ,
                            'Start'    : self.semi_static_vars ['START'   ], 
                            'End'      : self.semi_static_vars ['END'     ], 
                            'Data'     : self.semi_static_vars ['DATA'    ], 
                            'RestartAt': self.semi_static_vars ['RESTART' ],
                            'TreeData' : self.semi_static_vars ['TREEDATA'],
                            }

        else: 

            # fix this, add XD code_vars here 
            
  



            # create the function 
            function_code_string = '''def Finder'''+self.name+'''(START, CODE=input_CODE, DATA):'''
            function_code_string = function_code_string + Indent( UnIndent('''
            # initilize values
            FinderSwitchValue     = False
            FinderStart           = START
            FinderEnd             = START
            FinderData            = {}
            FinderRestartLocation = None
            TreeData              = {}
                ''', '            '))
            function_code_string = function_code_string + Indent(self.code) + Indent( UnIndent('''
            if FinderRestartLocation == None: FinderRestartLocation = FinderEnd 
                
            return { 
                'Found'     : FinderSwitchValue , 
                'Start'     : FinderStart, 
                'End'       : FinderEnd, 
                'Data'      : FinderData, 
                'RestartAt' : FinderRestartLocation,
                'TreeData'  : TreeData 
                   }\n''','            ')) 
            exec( function_code_string )
            # run the function with the inputs
            exec( '''finder_ = Finder'''+self.name+'''(input_START, input_CODE)\n''' )


            # { 
            #     'Found'    : FinderSwitchValue ,
            #     'Start'    : FinderStart, 
            #     'End'      : FinderEnd, 
            #     'Data'     : FinderData, 
            #     'RestartAt': FinderRestartLocation 
            #     'TreeData' : TreeData
            # }
            # if first in the finder chain, then the switch_value can be set
            if FIRST:
                self.switch_value                  = finder_['Found']        
                self.semi_static_vars ['START']    = finder_['Start']
                self.semi_static_vars ['END'  ]    = finder_['End']
                self.semi_static_vars ['DATA' ]    = finder_['Data']
                self.semi_static_vars ['RESTART']  = finder_['RestartAt']
                self.semi_static_vars ['TREEDATA'] = finder_['TreeData']

            FIRST = False 
            return finder_



#
#
#
# Finder Maker 
#
#
#

#Some tools 
def ReturnScoutsFromCommandsWith(attribute):
    global All_Commands 
    scouts_list  = []
    for each_command in All_Commands:
            for each_scout in each_command.ScoutsFor(attribute):
                scouts_list.append(each_scout)
    return scouts_list
# if you use InternalFind or InternalParse, set FIRST = False OR run it with input_START = *Starting point of the parent finder*
def InternalFind (input_Finder, input_START, input_CODE=CODE, input_DATA={}):
            return internal_Finder.SearchResults(input_START , input_CODE, input_DATA)
def InternalParse(Scouts      , input_START, input_CODE=CODE               ):
            global FIRST 

            #
            # Find which ones work
            #
            max_end_length = 0
            for each_scout in Scouts:
                    # reset some values
                    each_internal_scout = Scout(each_scout) # makes a copy of the scout in order to not interfere 
                    each_internal_scout.ClearMemory()       # clears the memory 


                    # test the scout 
                    # fix me, when this scout is Tested, all of the finders still have access to their own variables (such as SwitchValue) which could cause problems
                    scout_results = each_internal_scout.Test(input_START, input_CODE)





                    # if it wasn't found, remove it from the list
                    if not scout_results['Found']: 
                            Scouts.pop(each_internal_scout)
                    
                    # if found
                    else:
                       
                            # see if it is the largest 
                            if scout_results['End'] > max_end_length:
                                    
                                    # if it is, then clear the data of the old top_scout
                                    top_scout.ClearMemory()
                                    # make the current scout the new top_scout, and save it's data for later
                                    top_scout            = each_internal_scout
                                    top_scout.memory     = scout_results 
                                    # update the max so far 
                                    max_end_length = end_length 
            try:
                top_scout
            except NameError:
                FIRST = False
                return {'Found' : False }

            #
            # Deploy the Scout
            #
            
            # gives { 'RestartAt' : RestartAt , 'TreeData' : TreeData } 
            scout_results    = top_scout.Deploy()
            
            # add that found = True 
            scout_results['Found'] = True

            #
            #   End Main_Parse 
            #
            FIRST = False
            return scout_results
# more tools
def ReplaceQuotes( input_regex ):
    
    def ReplaceQuote(input_regex_string):
        first_quote = r'(?<!\\)"'
        second_quote = r'([A-Za-z0-9\._ ]+)"'
        if Is__RegexIn__String(first_quote+second_quote, input_regex_string):
            group_setup     = re.search( first_quote+second_quote , input_regex_string )
            return input_regex_string[  0 : group_setup.start() ] + '(' + '|'.join(cascade(list(group_setup.group(1)))) + ')' + input_regex_string[  group_setup.end() : len(input_regex_string)  ]
            # same thing as above broken down
            #content_        = group_setup.group(1)
            #content_as_list = list(content_)
            #cascade_        = cascade(content_as_list)
            #replacement_    = '(' + '|'.join(cascade_) + ')'
        else:
            return input_regex_string 


    new_string = ''
    while True:
        new_string = ReplaceQuotes(input_regex)
        if new_string == input_regex:
            break
        input_regex = new_string
    return input_regex
def ProcessColons( regex ):
    return  '('      +      '|'.join(       cascade_(     re.split(  r'(?<!\\\\):'  ,  regex  )     )         )         +         ')'
    # below has the same output as above 
    # def splice_colons        ( regex ):
    #     return re.split(r'(?<!\\\\):',regex)
    # regex    = ReplaceQuotes(input_regex)
    # spliced_ = splice_colons(regex)
    # cascade_ = '(' + '|'.join(cascade(spliced_)) + ')'


def RegexFinder( input_name , input_regex ):
    regex_with_quotes_fixed = ReplaceQuotes(input_regex)
    partial_regex_matcher   = ProcessColons(regex_with_quotes_fixed)
    return Finder(input_name , '''

# string length finder 
string_ = CODE [ START:START+1 ] 
temp_end = 0 
while Is__RegexIn__String(r\'\'\''''+partial_regex_matcher+'''\'\'\', string_ ):
        temp_end = temp_end + 1 
        string_ = CODE [ temp_end : temp_end + 1 ] 

# actually checking the code 
if Is__RegexIn__String ( r\'\'\''''+input_regex+'''\'\'\', CODE [ START:temp_end ] ): 
    FinderSwitchValue = True 
    FinderEnd = temp_end 
        
        ''')





class Thinker:
    def __init__(self, input_name):
        self.name = input_name






#
#
#
# Parsing 
#
#
#

FIRST       = True 
The_Counter = 0 
The_Tree    = {}
def Main_Parse(input_START):
    global FIRST 
    def AppendToTree(dict_):
        global The_Tree 
        global The_Counter
        if dict_ != None:
            The_Tree[  dict_['name']+The_Counter  ] = dict_ 
            The_Counter = The_Counter + 1
    def ReturnScoutsFromCommandsWith(attribute):
        global All_Commands 
        scouts_list  = []
        for each_command in All_Commands:
                for each_scout in each_command.ScoutsFor(attribute):
                    scouts_list.append(each_scout)
        return scouts_list
    #
    # Load Scouts
    #
    Scouts = ReturnScoutsFromCommandsWith('open code')
    # fix me, later have a mechanism that measures how big certain matchers are 
                # for example a function with only one argument would be pretty small 
                # and a function with 20 arguments would probably be long
            # the run all of the small ones first, and if non of the small ones match
            # then start running some of the bigger ones 


    #
    # Find which ones worked
    #
    max_end_length = 0
    for each_scout in Scouts:
            # reset some values
            FIRST = True     

            # test the scout 
            scout_results = each_scout.Test(input_START)


            # if it wasn't found, remove it from the list
            if not scout_results['Found']: 
                    Scouts.pop(each_scout)
            
            # if found
            else:

                    # see if it is the largest 
                    if scout_results['End'] > max_end_length:
                            
                            # if it is, then clear the data of the old top_scout
                            top_scout.ClearMemory()
                            # make the current scout the new top_scout, and save it's data for later
                            top_scout          = each_scout
                            top_scout.memory   = scout_results
                            # update the max so far 
                            max_end_length = end_length  
    
    # if no scouts were found, print an error 
    try:
        top_scout
    except NameError:
        print "At " + str(input_START)+ " I couldn't find a command that matched the following code :/"
        exit(0)
        

    #
    # Deploy the Scout
    #
    scout_results    = dict(  top_scout.Deploy()  ) 
    AppendToTree( scout_results["TreeData"] )

    # Reset all the scouts and finders
    # fix this, this is a really inefficient way to clear the finder switches
    for each_finder in All_Finders:
        each_finder.ResetSwitch()

    #
    #   End Main_Parse 
    #
    return scout_results["RestartAt"] 
def ParseAll(Code_):
    global The_Tree 
    while (starting_point <= len(Code_)):
        old_starting_point = starting_point 
        starting_point = Main_Parse(starting_point, Code_)
        if starting_point == old_starting_point: 
            print "probably in an infinite loop because something isn't parsing"
            break 


ParseAll(CODE)

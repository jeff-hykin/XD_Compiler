#import pdb          # debugging 
import random
import sys
import os
import regex as re
import itertools
import datetime
import pickle 
import sh
from math import *






#
# debugging 
#
if True:
        debug   = True
        COUNTER = 0
        COUNTER2 = 1
        COUNTER_for_Poke = 0
        def POKE      (input=0):
            if type(input) == str:
                    print input
                    exit(0)
            print "here"
            global COUNTER_for_Poke 
            COUNTER_for_Poke = COUNTER_for_Poke + 1 
            if COUNTER_for_Poke >= input:
                exit(0)
        INDENT = 0
        def TestPrint (input_):
            global INDENT
            if debug: print str(INDENT * '    ') + str(input_)


#
# File manipulation
#
if True:
        def pwd():
            return str( os.path.dirname(os.path.realpath(__file__)) )
        def Load      (string_):
          exec ('''global '''+string_+'''\n'''+string_ +"""= pickle.load(open(\""""+string_+'.pickle","rb"))')
        
        def Save      (name): 
            try:
                exec ('''pickle.dump('''+name+''', open("'''+name+'''.pickle","wb"))''')
                    #^ thats how my def Save() should work 
            except NameError:
                    # but it doesn't work when using it inside an exec()
                    # which is why the below lines are used to get around the problem 
                    global sudo_globals
                    if name not in sudo_globals:
                        for any_ in sudo_globals: 
                            if type(sudo_globals[any_]) == dict:
                                if name in sudo_globals[any_]:
                                    locals()[name] = sudo_globals[any_][name]
                    exec ('''pickle.dump('''+name+''', open("'''+name+'''.pickle","wb"))''')
        
        def FileAt    (file_location):
            file_     = open(file_location,'r+')
            file_as_string = file_.read()
            file_.close()
            return file_as_string

        def OverWrite (file_location, data):
            file_     = open(file_location,'w')
            file_.write("")

        def ExecAllIn (folder_location):
            original_location = str(sh.pwd())[0:-1]
            
            # change directory 
            if folder_location != "":
                folder_location = folder_location
                sh.cd(folder_location)
            
            
            # if there is nothing inside of the folder, return {}
            if str(sh.ls("-1")) is "":
                return {}

            # list the names of all the python files
            string_list_of_all_python_files = str(sh.grep(    sh.ls("-1")  , ".py"     ))
            list_of_all_python_files        = re.split(r' *\n', string_list_of_all_python_files)[0:-1]

            # get the files and run them 
            for each in list_of_all_python_files:
                exec( FileAt(each) )

            # go back to original_location
            sh.cd(original_location)
            return locals()
        

        def LoadAllIn (folder_location):
            original_location = str(sh.pwd())[0:-1]
            
            # change directory 
            if folder_location != "":
                sh.cd(folder_location)
            
            # list the names of all the python files
            string_list_of_all_python_files = str(sh.grep(    sh.ls("-1")  , ".pickle"     ))
            list_of_all_python_files = re.split(r'\.pickle *\n', string_list_of_all_python_files)[0:-1]

            # get the files and run them inside traduki 
            for each in list_of_all_python_files:
                Load( each )

            # go back to original_location
            sh.cd(original_location)
            return locals()



#
#   Regex
#
if True:
        def Is__RegexIn__String       (regexstring,string): 
            # the stupid $ doesn't actually match the end 
            # at least it doesn't when there's a \n at the end 
            # so to get around this, I append (?![\s\S]) to the end
            if regexstring[-1] == '$' and regexstring[-2] != '\\':
                regexstring = regexstring + r'(?![\s\S])'
            output = re.search(regexstring,string) 
            if output == None:
                return False
            return len(output.group(0))>0
        
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


#
#   General 
#
if True:
        def Range_(input_):
            return range(0,len(input_))
        def Indent       (input_,      indent_='    '):
            if type(input_) == str:
                if not Is__RegexIn__String(r'^ *\n',input_):
                    input_ = indent_ + input_ 
                return re.sub('\n','\n'+indent_ , input_) 
            elif type(input_) == list:
                for each_item in Range_(input_):
                    input_[each_item] = re.sub('\n','\n'+indent_, input_[each_item]) 
                return input_ 
        def Print     (input_ , indent=8 ,  depth_=-1):
            if type(input_) == dict:
                depth_ = depth_ + 1 
                this_level = depth_
                for each in input_:
                    if type(input_ [ each ]) == dict:
                        print ' '*indent*this_level + str(each)+ ' '*(12 - len(str(each))) + ':'
                        Print( input_ [ each ] , indent  , depth_ )
                    elif type(input_ [ each ]) == str:
                        if re.search(r'\n',input_[each]) != None:
                            print ' '*indent*this_level + str(each)+ ' '*(12 - len(str(each))) + ':'
                            print Indent(input_[each],' '*indent*(this_level+1))
                        else:
                            print ' '*indent*this_level + str(each)+ ' '*(12 - len(str(each))) + ': ' + input_[each]
                    else:
                        print ' '*indent*this_level + str(each) + ' '*(12 - len(str(each))) + ': ' + str(input_[each])
            elif type(input_) == list:
                for each in input_:
                    if type(each) == list:
                        for inside_each in each:
                            print inside_each , 
                    else:
                        print ' '*indent+ str(each) 
            else: 
                print input_
        def PrintError(input_string):
            print input_string
            exit(0) 
        def Overwrite__DictWith__Dict(main_dict, new_dict):
            z = main_dict.copy()
            z.update(new_dict)
            return z 
        def Unindent     (input_,      indent_='    '):
            if type(input_) == str:
                input_ = re.sub(r'^'+indent_, '' ,input_)
                return re.sub('\n'+indent_,'\n' , input_) 
            elif type(input_) == list:
                for each_item in Range_(input_):
                    input_[each_item] = re.sub(r'^'+indent_, ''  , input_[each_item])
                    input_[each_item] = re.sub('\n'+indent_,'\n' , input_[each_item])
                return input_ 
        def ConvertToASCII_List(text):
            return [ord(each_char) for each_char in text]
        def Swap__StringFrom__To__With__(input_string, start_, end_, replacement_):
            return input_string[0:start_] + replacement_ + input_string[end_:len(input_string)]

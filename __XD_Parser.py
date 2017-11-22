from _general_stuff import *
import copy






# this Code would normally be pulled from a file or sys.arg[0]
Code = """

ten_ = 10
thing_ << ten_ + 10

"""






#
# general tools
#
if True:
    debug = False

    # INDENT and TestPrint() are just for debugging
    # if you want to see the inner workings of everything just set debug = True
    INDENT = 0
    def TestPrint (input_):
        global INDENT
        if debug: print str(INDENT * '    ') + str(input_)
    def deepcopy (input_):
        output = {}
        if input_ == None:
            return None
        for each in input_.keys():
            if type(input_[each]) == dict:
                output[each] = deepcopy(input_[each])
            else:
                output[each] = input_[each]
        return output
    



#
# Initial Vars  
#
if True: 
        # TheTree is where all of the output data is stored
        TheTree = {}

        # Basically every function in this parser needs 
        # ParseContext or something similar to ParseContext 
        # as one of it's inputs (usually the last input)
        ParseContext = {
            'CODE'    : Code  ,
            'START'   : 0     ,
            'END'     : 0     ,
            'RESTART' : 0     ,    
            'TREE'    : {}    ,
            'SHARE'   : {}    ,
            'FIRST'   : False ,  
            'FOUND'   : False ,
            'OUTPUT'  : None,
            'InitialContext': {},
        }
        # make a copy of the ParseContext
        OriginalParseContextKeys = []
        NullContext = dict(ParseContext)
        ParseContext['SHARE']['CodeReplace'] = {}
        


#
# Scout Class
#
if True:
        all_scouts = []
        class Scout(object):
            
            # constructor 
            def __init__(self, input_name, input_code=''):
                self.name       = input_name 
                self.code       = input_code 
                self.attributes = [ 'allows pre-scouting' ]
                self.memory     = None
                all_scouts.append(self)
            

            def Search(self, GivenParseContext):
                ParseContext = dict(GivenParseContext)

                # this global INDENT stuff is used for debugging 
                # (recursive ouput more indented than initial output)
                if True:
                    global INDENT
                    TestPrint('Looking for '+self.name)
                    INDENT = INDENT + 1
                    TestPrint('First? = '+ str(ParseContext['FIRST']))
                    TestPrint('has memory of itself? = ' + str(self.memory is not None))

                # if this scout has already been searched then its shortcut will be set
                # so check to see if the shortcut has been set 
                # if it has been set, then just load the results from Scout.memory 
                # (rather than re-parsing)
                first_ = ParseContext['FIRST']
                if first_ and self.memory is not None:
                    TestPrint('Shortcut for '+self.name+' found')
                    INDENT = INDENT - 1
                    return self.memory 
                
                # create some envionment variables (FOUND, END, RESTART, etc) 
                # that the Scout's code will use when it is run 
                if True: 
                    
                    # run the Code Replacer 
                    if 'allows pre-scouting' in self.attributes:
                        TestPrint(    'Code before replacement:\n' + Indent(  ParseContext['CODE'],'    '*(INDENT+1)  )     )
                        for each in ParseContext['SHARE']['CodeReplace'].keys():
                            TestPrint(        'segement is:\n'+ Indent(   ParseContext['CODE'][ ParseContext['START']:len(ParseContext['CODE']) ]   ,   '    '*(INDENT+1)    )         )
                            TestPrint('regex is:'+r'^(\s*)'+each+r'\b')
                            ParseContext['CODE'] = ParseContext['CODE'][ 0:ParseContext['START'] ] + re.sub(r'^(\s*)'+each+r'\b',      '\g<1>'+ParseContext['SHARE']['CodeReplace'][each],  ParseContext['CODE'][ ParseContext['START']:len(ParseContext['CODE']) ]    ) 
                        TestPrint(    'Code after replacement:\n' + Indent(  ParseContext['CODE'],'    '*(INDENT+1)  )     )
                    
                    # the thing has not been found 
                    ParseContext['FOUND'] = False
                    # keep a copy of the Parse Context (now that FOUND = False)
                    ParseContextCopy = dict(ParseContext)
                    # setup an InitialContext variable for the Scout's code 
                    ParseContext['InitialContext'] = ParseContextCopy
                    # make END and RESTART null so they can be checked for changes
                    ParseContext['END']     = None
                    ParseContext['RESTART'] = None
                    ParseContext['Find']    = Find 
                
                
                
                # run the Scout's code with the ParseContext variables
                exec( "from _general_stuff import *\n"+self.code , ParseContext )


                # refine the output
                if True:  
                        # delete all the extra local variables 
                        things_to_delete = []
                        for each in ParseContext:
                            if each not in OriginalParseContextKeys:
                                things_to_delete.append(each)
                        for each in things_to_delete:
                            del ParseContext[each]

                        # output is a shortcut for simply making Find() the parse context
                        # ex: OUTPUT = Find('blah') would mean just use the END,SHARE,TREE, etc inside of OUTPUT
                        if ParseContext.get('OUTPUT', None) is not None:
                            ParseContext = ParseContext['OUTPUT']

                        # the below code sets the END and RESTART if either of them were not set
                        if   ParseContext['END'] is None and ParseContext['RESTART'] is None and ParseContext['FOUND']:
                             PrintError('I think there is a Scout that forgot to specify an END or RESTART')
                        elif ParseContext['END'] is None:
                             ParseContext['END'] = ParseContext['RESTART']
                        elif ParseContext['RESTART'] is None:
                             ParseContext['RESTART'] = ParseContext['END']
                        
                        # add scout name
                        ParseContext['ScoutName'] = self.name
                        

                #* set memory 
                if first_ is True:
                    self.memory = ParseContext
                # if it was first then everything after it will not be 
                # therefore First is now False
                ParseContext['FIRST'] = False 
                # return data
                INDENT = INDENT - 1
                if ParseContext['FOUND']:
                    TestPrint('Found '+self.name)
                else:
                    TestPrint('Failed to find '+self.name)
                return ParseContext 




#
# _Parsers 
# 
if True:
        # ParseBiggest(Attributes, ParseContext)
        # ParseBiggest([Attributes], ParseContext)
        def ParseBiggest(*arguments):
            # input handling 
            ParseContext = dict(arguments[-1])
            attributes_to_avoid = []
            if type(arguments[0]) == list and len(arguments) == 2:
                attributes = arguments[0]
            elif type(arguments[0]) == list and type(arguments[1]) == list and len(arguments) == 3:
                attributes = arguments[0]
                attributes_to_avoid = arguments[1]
            else:
                attributes = list(arguments[0:-1])
            
            # function start 
            global all_scouts 
            biggest_ = {} 
            original_parse_set = deepcopy(ParseContext)

            # for each scout 
            for each_scout in all_scouts:
                # skip the ones with the attributes_to_avoid
                skip = False 
                for any_attribute in attributes_to_avoid:
                    if any_attribute in each_scout.attributes:
                        skip = True 
                if skip == True:
                    continue
                    
                # else if a scout has any of the needed attributes
                for any_attribute in attributes:
                    if any_attribute in each_scout.attributes:
                        # try and find it 
                        ParseContext = each_scout.Search(deepcopy(original_parse_set))
                        # if it finds more area then the last-biggest one 
                        #FIXME, deal with tie-situations 
                        if ParseContext.get('END',0) > biggest_.get('END',0):  
                            #then it is now the biggest one
                            biggest_ = deepcopy(ParseContext)
                        break
            # if no scouts, then return None 
            if biggest_ == {}:
                return None
            # else return the biggest_ scout 
            else:
                return biggest_ 
        
        # MainParse is essentially just ParseBiggest() on a loop 
        def MainParse(ParseContext):
            global TheTree 
            global all_scouts
            counter = 0
        
            # Keep finding things till nothing more can be found  
            while True:
                counter = counter + 1    
                ParseContext['FIRST'] = True
                ParseContext['TREE'] = {}
                ParseContext['START'] = ParseContext['RESTART']
                TestPrint('\n\n\nStart is now: '+str(ParseContext['START']))
                ParseContext = ParseBiggest('open code', ParseContext)
                if ParseContext == None:
                    break 
                TheTree[ str(counter) + ParseContext.get('ScoutName', 'missing scoutname')] = ParseContext['TREE']
                for each in all_scouts:
                    each.memory = None
            #check for end of code (whitespace)




#
# Tools (Used inside of the Scout's code)
#
if True: 

        #
        #   Find()
        #
            # examples of valid uses
            #Find(Scout, ParseContext)
            #Find(Regex, ParseContext)
            #Find([attributes], ParseContext)
                def Find(*inputs_tuple, **kwargs):
                    inputs_      = list(inputs_tuple)
                    # the input prep data 
                    ParseContext = inputs_[-1]
                    ParseContext['START'] = ParseContext['RESTART']
                    
                    # if only one non-context input 
                    if len(inputs_) <= 2:
                        # FindScout 
                        if type(inputs_[0]) is Scout:
                            TestPrint('trying to find scout:'+str(inputs_[0].name))
                            return inputs_[0].Search(ParseContext)
                        # FindRegex 
                        if type(inputs_[0]) is str:
                            TestPrint('trying to find regex:'+str(inputs_[0]))
                            remaining_code = ParseContext['CODE'][  ParseContext['START'] : len( ParseContext['CODE'] )  ]
                            regex_result   = re.match(inputs_[0], remaining_code)
                            TestPrint('looking at:\n'+Indent(remaining_code,'    '*(INDENT+1)))
                            if regex_result is None or regex_result.span()[-1] is 0:
                                return NullContext
                            ParseContext['FOUND']            = True 
                            ParseContext['END']              = ParseContext['START'] + regex_result.span()[-1]
                            ParseContext['RESTART']          = ParseContext['END']
                            ParseContext['SHARE']['Content'] = remaining_code[  0  :  regex_result.span()[-1]   ]
                            ParseContext['ScoutName']        = 'FindRegex'
                            return ParseContext
                        # FindAttributes 
                        if type(inputs_[0]) is list:
                            TestPrint('trying to find anything with:'+str(inputs_[0]))
                            
                            if "without" in kwargs.keys():
                                output = ParseBiggest(inputs_[0], kwargs["without"], ParseContext)
                            else:
                                output = ParseBiggest(inputs_[0], ParseContext)

                            if output != None:
                                return output
                            else:
                                ParseContext['FOUND'] = False 
                                return ParseContext

                        
                            

        #
        #   Quick()
        #
            # QuickParagraphScout
            # QuickEasyScout
            # QuickAlgorithmInput
                def QuickParagraphScout(*KeyWord_or_NameAndKeyWord):
                    start_or_name_and_start = list(KeyWord_or_NameAndKeyWord)
                    if len(start_or_name_and_start) == 1:
                        scout_name = 'ParagraphScoutFor'+start_or_name_and_start[0]
                        start      = start_or_name_and_start[0]
                    elif len(start_or_name_and_start) == 2:
                        scout_name = start_or_name_and_start[0]
                        start      = start_or_name_and_start[1]
                    else:
                        PrintError("To many arguments for ParagraphScout")
                    return Scout( scout_name, Unindent("""
                    scout_results = Find(IndentScout, InitialContext )
                    if scout_results["FOUND"]:
                        indent_ = scout_results["TREE"]["Indent"]
                        num = scout_results['RestartAt'] 
                        scout_results = Find( RegexScout('"""+start+"""RegexScout', '\""""+start+"""\":\:'), scout_results )
                        if scout_results['FOUND']:
                            scout_results = Find(IndentedParagraphScout, scout_results)
                            if scout_results["FOUND"]:
                                FOUND    = True 
                                TREE = { 'Content' : scout_results["TREE"]["Content"] }
                                END      = scout_results["RESTART"]
                    #TREE
                        #Content : all of the input as a string
                    """))
                def QuickEasyScout(*KeyWord_or_NameAndKeyWord):
                    start_or_name_and_start = list(KeyWord_or_NameAndKeyWord)
                    
                    #Figure out the name
                    if len(start_or_name_and_start) == 1:
                        scout_name = 'ParagraphScoutFor'+start_or_name_and_start[0]
                        start      = start_or_name_and_start[0]
                    elif len(start_or_name_and_start) == 2:
                        scout_name = start_or_name_and_start[0]
                        start      = start_or_name_and_start[1]
                    else:
                        PrintError("To many arguments for QuickEasyScout")

                    return Scout( scout_name, Unindent('''
                    scout_results = Find( QuickParagraphScout("'''+start+'''") , InitialContext )
                    if scout_results['FOUND']:
                        FOUND   = True 
                        SHARE   = scout_results['SHARE']
                        TREE    = scout_results['TREE']
                        END     = scout_results['END']
                        RESTART = scout_results['RESTART']
                    else:
                        scout_results = Find( IndentScout , InitialContext )
                        if scout_results['FOUND']:
                            scout_results = Find( "'''+start+'''" , scout_results )
                            if scout_results['FOUND']:
                                scout_results = Find( "\:" , scout_results )
                                if scout_results['FOUND']:
                                    scout_results = Find( RestOfTheLineScout , scout_results )
                                    FOUND = True 
                                    SHARE = scout_results['SHARE']
                                    TREE  = scout_results['TREE']
                                    END   = scout_results['END']
                    '''))





        #
        #   Standard Scouts 
        #
            #Newline
                Newline = Scout('Newline') 
                Newline.code = '''OUTPUT = Find(r"\\n", InitialContext)'''
            #Newlines
                Newlines = Scout('Newlines') 
                Newlines.code = '''OUTPUT = Find(r"\\n+", InitialContext)'''
            #SpacesOrNothing
                #FIXME probably an issue here with 0 spaces 
                SpacesOrNothing = Scout('SpacesOrNothing')
                SpacesOrNothing.code = '''OUTPUT = Find(r" *", InitialContext)'''
            #WhiteSpace
                WhiteSpace = Scout('WhiteSpace')
                WhiteSpace.code = '''OUTPUT = Find(r"( |\\n|\\t)*", InitialContext)'''
            #IndentScout
                IndentScout = Scout('IndentScout')
                IndentScout.code =  Unindent('''
                if START is 0 or CODE[START-1] == '\\n': 
                    OUTPUT = Find(r" *", InitialContext)
                    if OUTPUT['FOUND']:
                        OUTPUT['SHARE']['Indent'] = OUTPUT['SHARE']['Content']
                ''', '                ')
            #NormalStart
                NormalStart = Scout('NormalStart')
                NormalStart.code = Unindent('''
                results = Find(Newlines, InitialContext)
                if START is 0 and results['FOUND'] is False:
                    OUTPUT = Find(IndentScout, InitialContext)
                else:
                    OUTPUT = Find(IndentScout, results)
                    Print(OUTPUT['END'])        
                ''' ,'                ' )
            #EndOfLineScout
                
            #WholeRestOfTheLineScout
            #RestOfTheLineScout
            #IndentedParagraphScout
            #NumberScout
            #CommaSeperatorScout
            #CommaOrSpaceSeperatorScout





#
#  import scouts 
#
if True: 
    # exec(FileAt(pwd()+"/*thing_name*.py"))
    exec(FileAt(pwd()+"/Scouts/EqualScout.py"))
    exec(FileAt(pwd()+"/Scouts/AssignmentScout.py"))
    exec(FileAt(pwd()+"/Scouts/UserNamedValueScout.py"))
    exec(FileAt(pwd()+"/Scouts/ExistingUserNamedValueScout.py"))
    exec(FileAt(pwd()+"/Scouts/RawNumberScout.py"))
    exec(FileAt(pwd()+"/Scouts/PlusOperatorScout.py"))
    for each in all_scouts:
        ParseContext[each.name] = each
    for each in ParseContext.keys():
        OriginalParseContextKeys.append(each)








MainParse(ParseContext)
print "the demo input:\n" + Indent(Code)
Print( TheTree )









AssignmentScout = Scout('AssignmentScout')
AssignmentScout.attributes.append('open code')

AssignmentScout.code = r'''

# create ExistingNamedValues if it doesnt exist 
if SHARE.get('ExistingNamedValues') == None:
    SHARE['ExistingNamedValues'] = {}



# find the Name
scout_results = Find(UserNamedValueScout, InitialContext)
if scout_results['FOUND']:
    name_ = scout_results['SHARE']['Name']
    
    # find the assignment symbol
    #FIXME: change how symbols are found  
    scout_results = Find(r' *<<', scout_results)
    if scout_results['FOUND']:
        
        # find the value
        scout_results = Find(['Value'], scout_results)
        if scout_results['FOUND']:
            # report found 
            
            FOUND   = True 
            END     = scout_results['END']
            RESTART = scout_results['RESTART']
            
            # record the new value 
            #SHARE['ExistingNamedValues'][name_] = SHARE['ExistingNamedValues'].get(name_, {'Range':[]})
            #SHARE['ExistingNamedValues'][name_]['Range'].append(scout_results['TREE']['Range'])
            
            # update the tree 
            TREE['Assignment'] = scout_results['TREE']
            TREE['Assignee']   = name_

        '''
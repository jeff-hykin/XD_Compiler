SymbolScout = Scout('SymbolScout')
SymbolScout.attributes.append('Value')

SymbolScout.code = '''
SHARE['Content'] = []

# FIXME, add the TREE values for everything that is found 


# prevent recursive
if SHARE.get('SymbolRecursion') == True:
    FOUND = False
else:
    nothing_has_been_found = True 
    symbol_has_been_found = False 
    scout_results = None
    last_found = None 
    while True:
        # look for symbols first 
        if nothing_has_been_found:
            scout_results = Find(['Symbol'], InitialContext)
        else:
            scout_results = Find(['Symbol'], scout_results)
        if scout_results['FOUND']:
            last_found = scout_results
            nothing_has_been_found = False 
            symbol_has_been_found = True
            SHARE['Content'].append(scout_results['Content'])
            continue
        
        # then look for values 
        else:
            # set a flag to prevent infinite recursion 
            SHARE['SymbolRecursion'] = True
            
            if nothing_has_been_found:
                scout_results = Find(['Value'], InitialContext)
            else:
                scout_results = Find(['Value'], scout_results)
            if scout_results['FOUND']:
                last_found = scout_results
                nothing_has_been_found = False 
                SHARE['Content'].append(scout_results['SHARE']['Content'])
                continue
        
        # if nothing was found fail 
        if nothing_has_been_found or not symbol_has_been_found:
            FOUND = False
            break
        # if something was found once but then on the next loop nothing was, then end 
        else:
            FOUND   = True
            END     = last_found['END']
            RESTART = last_found['RESTART']
'''


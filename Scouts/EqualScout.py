EqualScout = Scout('EqualScout')
# remove pre scouting, then add open code 
EqualScout.attributes = ['open code']

#FIXME: remeber to add the star replacement *replacement*
#FIXME: remeber to add evaluate replacements 
#FIXME: use Indent instead of just skimping with r'\s*'

EqualScout.code = r'''
# initilize some things 
if SHARE.get('ExistingNames') == None:
    SHARE['ExistingNames'] = []

#find the name
scout_results = Find(r'\s*[\w_]+', InitialContext )
if scout_results['FOUND']:
    
    #check the name 
    name_ = re.sub( '\s*(.+)', '\g<1>', scout_results['SHARE']['Content'])
    if name_ in SHARE['ExistingNames']:
        PrintError('Sorry, but I think '+name_+' has already been used somewhere else in the instructions')
    else:
        SHARE['ExistingNames'].append(name_)
    
    # get equal sign out of the way 
    scout_results = Find(' *=', scout_results)
    if scout_results['FOUND']:
        
        
        # grab the content 
        scout_results = Find('.+', scout_results)
        if scout_results['FOUND']:
            
            # check the content for recursion 
            # FIXME: this method might be flawed 
            if True:
                for each in SHARE['CodeReplace'].keys():
                    CODE[ START:len(CODE) ] = re.sub(r'^(\s*)'+each+r'\b',      '\g<1>'+SHARE['CodeReplace'][each],  CODE[ START:len(CODE) ]    ) 
                
                if Is__RegexIn__String(r'^(\s*)'+name_+'\b', CODE[ START:len(CODE) ] ):
                    # if it's not equal to itself, then give an error
                    if not Is__RegexIn__String(r'^(\s*)'+name_+'[^\n\S]*(\n|$)', CODE[ START:len(CODE) ] ):
                        PrintError('I think there is some impossible recursion with '+ name_ )
                        #FIXME: add some details to this error ^ 
            
            # record the new replacement 
            SHARE['CodeReplace'][ name_ ] = scout_results['SHARE']['Content']
            FOUND   = True 
            END     = scout_results['END']
            RESTART = scout_results['RESTART']
            TREE    = {'Name': name_, 'Code':scout_results['SHARE']['Content']}
            '''
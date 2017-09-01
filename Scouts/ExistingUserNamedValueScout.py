ExistingUserNamedValueScout = Scout('ExistingUserNamedValueScout') 
ExistingUserNamedValueScout.attributes.append('NamedValue')
ExistingUserNamedValueScout.attributes.append('Value')
#SHARE's 
    #Name    (string)
 
ExistingUserNamedValueScout.code = r'''
if SHARE.get('ExistingNamedValues') == None:
    SHARE['ExistingNamedValues'] = {}
else:
    results = Find(r'(?: +|\n|)([a-z]+_[a-z_]*)(?![a-zA-Z_])', InitialContext)
    if results['FOUND']:
        # get the name 
        name_ = results['SHARE']['Content']
        name_ = re.sub(r'(?: +|\n|)(.+)', '\g<1>', name_)
        if name_ in SHARE['ExistingNamedValues']:
            FOUND   = True
            END     = results["END"]
            RESTART = results["RESTART"]
            
            TestPrint('NamedValue found '+ name_)
            SHARE['Name']  = name_ 
            TREE['Range']  = SHARE['ExistingNamedValues'][name_]['Range']
            TREE['Range']['Form'] = 'Raw'
'''
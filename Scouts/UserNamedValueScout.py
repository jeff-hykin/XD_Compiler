UserNamedValueScout = Scout('UserNamedValueScout') 
UserNamedValueScout.attributes.append('NamedValue')
#SHARE's 
    #Name    (string)
 
UserNamedValueScout.code = r'''
if SHARE.get('ExistingNamedValues') == None:
    SHARE['ExistingNamedValues'] = {}

results = Find(r'(?:\n| *)([a-z]+_[a-z_]*)(?![a-zA-Z_])', InitialContext)
if results['FOUND']:
    FOUND   = True
    END     = results["END"]
    RESTART = results["RESTART"]
    
    # get the name 
    name_ = results['SHARE']['Content']
    name_ = re.sub(r'(?: +|\n|)(.+)', '\g<1>', name_)
    SHARE['Name'] = name_ 
'''
RawNumberScout = Scout('RawNumberScout')
RawNumberScout.attributes.append('Value')
RawNumberScout.attributes.append('RawValue')
RawNumberScout.code = r'''
scout_results = Find(r'(?: +|\n|)(-|)(\d*\.\d+|\d+)', InitialContext )
if scout_results['FOUND']:
    number_ = scout_results['SHARE']['Content']
    number_ = re.sub(r'(?: +|\n|)(.+)', '\g<1>' , number_ )
    
    FOUND = True 
    END   = scout_results['END']
    RESTART = scout_results['RESTART']
    type_ = ''
    
    if eval(number_) % 1 == 0:
        type_ = 'int'
    else:
        type_ = 'double'
    TREE['RawNumber'] = { 'Value': number_ , 'Type' : type_ } 
    '''
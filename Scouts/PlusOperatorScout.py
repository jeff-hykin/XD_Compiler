PlusOperatorScout = Scout('PlusOperatorScout')
PlusOperatorScout.attributes.append('Value')
PlusOperatorScout.attributes.append('OperatorValue')
PlusOperatorScout.code = r"""
# find argument1
results = Find(['NamedValue'], InitialContext)
if not results['FOUND']:
    results = Find(['RawValue'],InitialContext)
    if not results['FOUND']:
        results = Find(['StatementValue'], InitialContext)
        if not results['FOUND']:
            results = Find(ParethesesValueScout)
if results['FOUND']:
    argument1 = results['TREE']
# find the operator 
    results = Find(r' *\+ *', results)
    if results['FOUND']:
# find argument2
        after_operator = results
        results = Find(['NamedValue'], after_operator)
        if not results['FOUND']:
            results = Find(['RawValue'],after_operator)
            if not results['FOUND']:
                results = Find(['StatementValue'], after_operator)
                if not results['FOUND']:
                    results = Find(ParethesesValueScout)

        if results['FOUND']:
            argument2 = results['TREE']
            
            # by default it returns int
            return_type = 'int'
            # if either of the arguments Type is double, then change return_type to double
            if argument2[argument2.keys()[0]]['Type'] == 'double' or argument1[argument1.keys()[0]]['Type'] == 'double':
                return_type = 'double'
            FOUND = True
            END = results['END']
            RESTART = results['RESTART']
            TREE['PlusOperator']  = {}
            TREE['PlusOperator']['Argument1'] = argument1
            TREE['PlusOperator']['Argument2'] = argument2
            TREE['PlusOperator']['Type']      = return_type
"""



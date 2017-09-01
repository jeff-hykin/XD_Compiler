ParenthesesValueScout = Scout('ParenthesesValueScout')
ParenthesesValueScout.code = r"""
results = Find(r' *(', InitialContext)
if results['FOUND']:
    results = Find(['Value'], results)
    if results['FOUND']:
        value_data = results
        results = Find(r' *)',results)
        if results['FOUND']:
            TREE    = value_data
            FOUND   = True
            END     = results["END"]
            RESTART = results["RESTART"]
"""
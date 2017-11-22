# Heads up

This is my most ambitious project, and at the moment it is not a great representation of my code in general. If you know how to use it, it works reliably. However, it is far from being finished. I suggest reading 'how it works' to get a good idea of the program, but you might want to wait till a later date before looking at the code.

The program needs a good coding-interface (even if you know how to use it, it is currently a pain to use). I'll likely be able to build an interface around Jan 2017. Until the interface is made, it is posted here more for ease of access (rather than collaboration). The other major design element that needs to be fixed are the coding methods/pratices. There are many uses of exec() which (if it wasn't obvious) is a terrible terrible thing to be using frequently.

# Demo
If you'd still like to get a quick feel for the project, clone the repo, and run the parser file. It parses some demo code and prints the syntax tree for the code. 

# How it works
The parser works by importing Scout objects, which you could think of as regular expressions--if regular expressions were easy to read and could contain advanced programming logic like loops and if statements. The Scout objects are the definition of different things: phone_number_Scout, email_Scout, if_statement_Scout, assignment_Scout, function_defintion_Scout, infix_operator_Scout, etc. 

Here is an example of a crude but legitimate phone_number_Scout that essentially just relies on regular expressions
```
phone_number_Scout = Scout('phone_number_Scout')
phone_number_Scout.code = """

// Find a match for the regular expression of a phone number, and find it in the InitialContext
scout_results = Find(r'\d\d\d( |-|)\d\d\d( |-|)\d\d\d', InitialContext )
if scout_results['FOUND']:
    // if the regex was found, then the phone number scout was found
    FOUND   = True

    // RESTART will almost always be the index of the end of whatever you found
    // however, sometimes you might want to look ahead, 
    // and then restart somewhere before the end of whatever you looked at
    RESTART = scout_results['RESTART']
    
    everything_the_regex_found = scout_results['SHARE']['Content']
    
    // get rid of the dashes and/or spaces in the phone number
    phone_num_as_string = re.sub(r'( |-|)','',everything_the_regex_found)
    
    // what data you'd like to share if another Scout were to use this Scout
    SHARE    = {'PhoneNumber':phone_num_as_string} 

"""
```

The big advantage of the parser is that Scouts can find other Scouts recursively. For example the phone-number Scout can call the number Scout. This is extremely useful for more advanced parsing, for example the if_statement_Scout can look for "if" and then look for the conditional_expression_Scout. It also makes things like finding matching parentheses trivial. (Even though the current syntax is too verbose)

```
nested_parentheses_Scout = Scout('nested_parentheses_Scout')
nested_parentheses_Scout.code = """

// find the first parenthese and the non-parenthese chars after it
first_search = Find(r'\([^\(\)]*',InitialContext):
if first_search['FOUND']:
    // if the first parenthese was found, then look for a closing one
    second_search = Find( r'\)',first_search )
    // if the closing one was found, then we're done
    if second_search['FOUND']:
        FOUND = True
        RESTART = second_search['RESTART']
        SHARE = {'Content': first_search['SHARE']['Content'] + second_search['SHARE']['Content'] }

    // if the closing parenthese wasnt immediately found, then become recursive
    else:
        alternative_second_search = Find(nested_parentheses_Scout, first_search)
        if alternative_second_search['FOUND']:
            FOUND = True
            RESTART = alternative_second_search['RESTART']
            SHARE = {'Content': first_search['SHARE']['Content'] + alternative_second_search['SHARE']['Content'] }
"""
```

The above Scout will work for a simple example, but it would need a decent amount of edits to become a useful parenthese matcher.

Scouts can also be given attributes. For example, `equivlence_expression_Scout` can be given the attribute `'conditional statement'`, and then `comparision_expression_Scout` can also be given `'conditional statement'` and then `Find(['conditinal statement'])` will search for all scouts with the conditinal statement attribute. 

Overall the XD_Parser is build to be extremely flexible/powerful, while still being easily readable. Obviously it still needs work on becoming readable. For now there are only a few demo Scout objects, and some demo input. However, in the distant future their will be a standard library of Scouts that will hopefully be able to quickly parse many programming languages.

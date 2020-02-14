# comparse

<p><b>COMPARSE - JUST LIKE ARGPARSE, ONLY BETTER!</b> <br />
Comparse (short for "command parser") is a simple, flexible argument parser. Designed to pick out ATTRIBUTES and assign VALUES to them from a message containing many un-formatted attributes/variables. It uses the Python <code>shlex</code> and <code>difflib</code> modules. I have included the module in this repository.
<br>
<br/><p><b>FEATURES</b>
<br/>* User-friendly
<br/>* Easy-to-use
<br/>* Accomodates spelling, grammar and syntax errors in the user-input by leveraging Python <code>difflib</code> module
<br/>* Relatively fast compared to NLP modules
</p>
<br/><p><b>USAGE</b> <br />
I used a physics parser in examples A - F. The parser accepts values for mass and velocity and assigns them to a dictionary with keys 'mass' and 'vel' as specified. Examples G - I demonstrate other capabilities.  

    #A. The test message you wish to process.
    message = "I have two variables: -mass: 12 --vel= 18"

    #B. Create a parser object. "True" if you wish to suppress the help message from being displayed. 
    physics = comparse(True)

    #C. Tell the parser what arguments it should accept.
    physics.add_argument("vel", "int", 10, "this is your velocity attribute")
    physics.add_argument("mass", "float", 10, "this is your mass attribute")  

    #D. Give the parser a specific message for which it should extract arguments.
    print(physics.parse(message))
    
    #E. Extract a list of sorted values after the message has been parsed.
    print(physics.sorted_values())
    
    #F. Extract string after attribute-value pairs have been removed.
    print(physics.remove_all_attributes())
    
    #G. Detect a value with a unit of measure within a message.
    message2 = 'The temperature in this room is too cold, crank it up to 27.6 degree please.'
    print(query.find_unit_value(message2, 'temperature', 'degree'))

    #H. Detect single character attributes. I used D&D gaming dice as an example.
    message3 = "d10+5 + 1 d 20 for parried attack + 4d12 to smite + 1d10"
    query.add_argument("d", int, 20, "XdY+n")
    print(query.parse(message3)['d'])
    
    #I. Detect values PRIOR to attributes
    print(query.parse(message3, reverse=True)['d'])
</p>

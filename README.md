# comparse

<p><b>COMPARSE - JUST LIKE ARGPARSE, ONLY BETTER!</b> <br />
Comparse (short for "command-line parser") is a simple, flexible argument parser. Designed to pick out ATTRIBUTES and assign VALUES to them from a message containing many un-formatted attributes/variables. It uses the Python <code>shlex</code> module. I have included the module in this repository.
</p>
<br>
<b>UPDATE (23 Jul 2019):</b> now with <code>difflib.get_close_matches</code> to approximate attribute names within strings, in the event the user had misspelled the attribute.
<br>
<p><b>USAGE</b> <br />
I used a physics parser as an example. The parser accepts values for mass and velocity and assigns them to a dictionary with keys 'mass' and 'vel' as specified by the parser. 

    #The test message you wish to process.
    message = "I have two variables: -mass: 12 --vel= 18"

    #Create a parser object. "True" if you wish to suppress the help message from being displayed. 
    physics = comparse(True)

    #Tell the parser what arguments it should accept.
    physics.add_argument("vel", "int", 10, "this is your velocity attribute")
    physics.add_argument("mass", "float", 10, "this is your mass attribute")  

    #Give the parser a specific message for which it should extract arguments.
    print (physics.parse(message))
</p>

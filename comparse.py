'''COMPARSE - JUST LIKE ARGPARSE, ONLY BETTER!
Comparse is a flexible commandline parsing module. Designed to pick out ATTRIBUTES and assign VALUES to them from a message containing many un-formatted attributes/variables.
- message: the actual message,
- attribute: the actual attribute (variable) you wish to extract from the message,
- var_type: variable type, this accepts integers, string, float variables,
- default: the default value of the attribute,
- help_txt: the help text you wish to display,
- suppress_help_txt: if True, help_txt will not be displayed. 
'''

import shlex
class comparse(object):
    def __init__(self, suppress_help_txt):
        self.data = {}   #This is the "data" dictionary that this function will ultimately return.
        self.attributes = []
        self.var_types = []
        self.defaults = []
        self.help_txts = []
        self.suppress_help_txt = suppress_help_txt

    def parse(self, message):  
        try:
            #Shows the help text if the user requests it.
            if(("-h" or "--help") in message):
                print("\nComparse is a flexible commandline parsing module. Designed to pick out ATTRIBUTES and assign VALUES to them from a message containing many un-formatted attributes/variables.")
                comparse.show_help(self)

            #Remove unwanted symbols (e.g. "=", ":", etc.)
            message = message.replace("=", " ")
            message = message.replace(":", " ")
            args = shlex.split(message)

            for attribute, var_type in zip(self.attributes, self.var_types):
                options = {k.strip('-'): True if v.startswith('-') else v
                    for k,v in zip(args, args[1:]+["--"]) if k.startswith('-') or k.startswith('')}
                if (var_type == "int"):
                    self.data[attribute] = int(options[attribute])   #Updates if "attribute" exists, else adds "attribute".
                if (var_type == "str"):
                    self.data[attribute] = str(options[attribute])   #Updates if "attribute" exists, else adds "attribute".
                if (var_type == "float"):
                    self.data[attribute] = float(options[attribute])   #Updates if "attribute" exists, else adds "attribute".
        except:
            #Shows the nice help text if suppress_help_txt is False.
            if not self.suppress_help_txt:
                comparse.show_help(self)

            for attribute, var_type, default in zip(self.attributes, self.var_types, self.defaults):
                #Searches for arguments that are actually IN the message.
                if attribute in message:
                    if (var_type == "int"):
                        self.data[attribute] = int(options[attribute])   #Updates if "attribute" exists, else adds "attribute".
                    if (var_type == "str"):
                        self.data[attribute] = str(options[attribute])   #Updates if "attribute" exists, else adds "attribute".
                    if (var_type == "float"):
                        self.data[attribute] = float(options[attribute])   #Updates if "attribute" exists, else adds "attribute".
                
                #Adds default values to attributes that are NOT in the message.
                if attribute not in message:
                    if (var_type == "int"):
                        self.data[attribute] = int(default)   #Updates if "attribute" exists, else adds "attribute".
                    if (var_type == "str"):
                        self.data[attribute] = str(default)   #Updates if "attribute" exists, else adds "attribute".
                    if (var_type == "float"):
                        self.data[attribute] = float(default)   #Updates if "attribute" exists, else adds "attribute".
        return self.data
    
    #This method shows the formatted help text.
    def show_help(self):
        print("\n usage:")
        for attribute, help_txt in zip(self.attributes, self.help_txts):
            print("    "+ "-"+attribute+"="+str(attribute).upper() + ", -"+attribute+":"+str(attribute).upper() + ", -"+attribute+" "+str(attribute).upper() + "\t["+help_txt+"]")
        print("    [note that if an attribute is not specified, then its specified default value is used]")
        print("\n optional arguments:")
        print("    -h, --help\t\t\t\t[show this help message and exit] \n")

    #This method collects all attributes from the "outside world" into arrays and passes them into the parse function within the local environment.
    def add_argument(self, attribute, var_type, default, help_txt):
        self.attributes.append(attribute)
        self.var_types.append(var_type)
        self.defaults.append(default)
        self.help_txts.append(help_txt)


'''COMPARSE - A SIMPLE NLP MODULE FOR PARSING TEXT MESSAGES
Comparse is a flexible commandline parsing module. Designed to pick out ATTRIBUTES and assign VALUES to them from a message containing 
many un-formatted attributes/variables. Module and documentation by TheMachinePreacher (the.machine.preacher@gmail.com), 14 Jul 2018.
- message: the actual message,
- attribute: the actual attribute (variable) you wish to extract from the message,
- var_type: variable type, this accepts integers, string, float variables,
- default: the default value of the attribute,
- help_txt: the help text you wish to display,
- suppress_help_txt: if True, help_txt will not be displayed, 
- reverse: if TRUE, parses the message for values PRIOR to the attribute,
- find_unit_value: detects a value with a unit of measure within a message,
- NOTE: the entire substring following an attribute marker will be parsed. This function outputs a dictionary containing LISTS.
'''

import shlex, re, difflib
class comparse:
    def __init__(self, suppress_help_txt):
        self.data = {}   # This is the "data" dictionary that this function will ultimately return.
        self.attributes = []
        self.retrieved_attributes = [] # This are a list of attributes that were found in the message.
        self.var_types = []
        self.defaults = []
        self.help_txts = []
        self.error_log = "Invalid entry (or none) for the following variables, default values were used instead (-h for help):"
        self.suppress_help_txt = suppress_help_txt

    def __repr__(self):
        return """\t* Command parsing for this program was done using COMPARSE: a flexible commandline parsing module.
        * Designed to pick out ATTRIBUTES:VALUES pairs in a message.\n"""

    def parse(self, message, reverse=False):  
        # Initialize variables
        self.reverse = reverse # This parses the message for values PRIOR to the attribute.
        help_list = [] # help_list variable.

        # Shows the help text if the user requests it.
        if(("-h" or "-help") in message or message.endswith("-h")):
            help_list = [attribute for attribute in self.attributes if attribute in message] # Prepare only requested help text. 
            if not help_list: help_list = self.attributes # If no specific help requested, prepare them all!
            if not self.suppress_help_txt:
                self.error_log = comparse.show_help(self, help_list)
                return self.error_log

        # Remove unwanted symbols (e.g. "=", ":", "[]", "()", "{}", etc.)
        message = message.replace("=", " ")
        message = message.replace(":", " ")
        message = message.replace("'", "")
        message = message.replace('"', "")
        message = message.replace("[", '')
        message = message.replace("]", '')
        message = message.replace("(", '')
        message = message.replace(")", '')
        message = message.replace("{", '')
        message = message.replace("}", '')
        message = message.replace("\n", '')
        message = " "+message
        
        # This allows mathematical symbols to be used by ensuring that only a single space surrounds characters not 
        # surrounded by spaces or surrounded by multiple spaces.  
        message = re.sub(r'\s*([<>+*/-])\s*', ' \\1 ', message)

        # This segregates any int and float values from text within the message.
        message = re.sub(r'\s*([0-9.]+)\s*', ' \\1 ', message)

        # Temporarily store the message in the self.message variable for easy retrieval by other methods.
        self.message = message
        
        # The code below attempts to match attributes that are partially specified in the message, in many possible combinations. 
        # It also automatically corrects the main self.message variable. 
        def attribute_match(string, match):
            # Conforms the message to accomodate attributes that are single characters.
            string = re.sub("r'(?<=[0-9])\s*("+match+")\s*(?=[0-9])'", ' \\1 ', string)
            string = re.sub("r'\s*("+match+")\s*(?=[0-9])'", ' \\1 ', string)
            string = re.sub("r'("+match+")\s*(?=[0-9])'", ' \\1 ', string)

            # Attempts to match whole words exactly. 
            for word in string.split(): 
                if match == word: 
                    self.message = string.replace(match+' ', match+'  ') # Prevents adjacent matches from 'grabbing' each other.
                    return match
            # Finds the closest match and conforms the original message to fit the attribute. Possibilities that don’t score at least 
            # 0.7 for similarity to the match are ignored.
            if len(match) > 4: # Only activate difflib if the match string is greater than 4 characters long.
                if difflib.get_close_matches(match, string.split(),3,0.7): 
                    # This prevents adjacent matches from 'grabbing' each other.
                    self.message = string.replace(difflib.get_close_matches(match, string.split())[0]+' ', match+'  ') 
                    return match

        # This reverses a list and searches for values PRIOR to the attribute.
        if self.reverse: message = " ".join(list(reversed(message.split(" "))))

        # This returns a SET of attributes (it filters out duplicates and empty values).
        attributes = []
        for attribute in self.attributes: 
            attributes.append(attribute_match(message, attribute))
            attributes = list(set(attributes))
            attributes = self.retrieved_attributes = [x for x in attributes if x is not None]
        
        # Conforms the original message to fit the attribute.
        message = self.message

        # Insert quotation marks after string attributes. This will ensure that the entire substring 
        # following an attribute marker is correctly parsed. # This function matches the entire attribute 
        # found in the sentence so that quotation marks can be applied accurately to the string. 
        for attribute in attributes:
            modified_attribute = ' '+attribute+' '
            message = modified_attribute.join(f'"{s}"' for s in message.split(modified_attribute))
            if attributes.index(attribute)>0: message = message[1:-1]

        # This splits the message into words, a process similar to tokenizing words.
        args = shlex.split(message) # This splits the message. 
        
        # This section declares 'temp_options' and 'options' dictionaries and populates them.
        temp_options = {}
        options = {}
        for k,v in zip(args, args[1:]): temp_options[k] = []
        
        # This populates the 'temp_options' dictionary.
        for k,v in zip(args, args[1:]): 
            for item in [x.strip(' ') for x in v.split(",")]: temp_options[k].append(item) # Split elements by comma.
        
        # This picks out only attributes specified in the message and populates the other, 
        # unspecified attributes with default values. 
        for attribute in self.attributes: 
            if attribute in list(temp_options.keys()) and temp_options[attribute]: 
                options[attribute] = temp_options[attribute]
            else: 
                options[attribute] = [self.defaults[self.attributes.index(attribute)]]
                # Note in error log.
                help_list.append(attribute)
                for i in help_list: 
                    if i not in self.error_log : self.error_log += ", " + i 
        
        # This section declares 'data' dictionary and populates it.
        self.data = {}
        for attribute in self.attributes: self.data[attribute] = []
        # This applies the correct variable type to the individual variables. 
        # Also provides for error-checking and logging. 
        for attribute, var_type, default in zip(self.attributes, self.var_types, self.defaults):
            # Appends the default value if none are specified, appends default values even if values have been 
            # partially specified by the user.
            for element in options[attribute]: 
                # NOTE Segregate the numbers from the strings! 
                if var_type is int and not type(element) is int: 
                    if type(element) is str:
                        for sub_element in element.split(" "): 
                            try: 
                                element = int(re.sub(r"([A-Za-z<>+*/-]+)", "", sub_element))
                                break # Find the first interger then break the loop immediately, 
                                      # don't look for anything else!
                            except: pass 
                if var_type is float and not type(element) is float: 
                    if type(element) is str:
                        for sub_element in element.split(" "): 
                            try: 
                                element = float(re.sub(r"([A-Za-z<>+*/-]+)", "", sub_element))
                                break # Find the first floating-point number then break the loop immediately, 
                                      # don't look for anything else!
                            except: pass 
                
                # NOTE Now fit everything together!
                try:
                    # Cater for user errors, invalid entries, boolean and None variables.
                    if element=="True" or element=="true" or element=="TRUE": self.data[attribute].append(bool(1))
                    elif element=="False" or element=="false" or element=="FALSE": self.data[attribute].append(bool(0))
                    elif element is None: self.data[attribute].append(None)
                    else: self.data[attribute].append(var_type(element))   
                except: 
                    # Note in error log.
                    help_list.append(attribute)
                    for i in help_list: 
                        if i not in self.error_log : self.error_log += ", " + i 
                    # Cater for user errors, invalid entries, boolean and None variables.
                    if default=="True" or default=="true" or default=="TRUE": self.data[attribute].append(bool(1))
                    elif default=="False" or default=="false" or default=="FALSE": self.data[attribute].append(bool(0))
                    elif default is None: self.data[attribute].append(None)
                    else: self.data[attribute].append(var_type(default))
                
        # Reverse the order of the detected values to corresponde to the sequence of the message.
        if self.reverse: self.data[attribute].reverse()
        # Return the output.
        return self.data
    
    # This method shows the formatted help text. Note that the printed text may be different 
    # from that which is returned by the method. Allows for greater flexibility.
    def show_help(self, help_list):
        show_help = "" # Text variable to be returned.
        # Collate help text into a neat variable to be returned by the method.
        show_help += "\nCommand parsing for this program was done using COMPARSE: a flexible commandline parsing module." 
        show_help += "\nDesigned to pick out ATTRIBUTES:VALUES pairs in a message."
        show_help += "\n\n usage:\n"
        for attribute, help_txt, var_type, default in zip(self.attributes, self.help_txts, self.var_types, self.defaults):
            # Only show requested help, don't bombard the user with everything!
            if attribute in help_list:
                show_help += "\n"+attribute
                show_help += "\n    "+help_txt+"\n"
                show_help += "    VARIABLE TYPE: "+var_type.__name__+"\n"
                show_help += "    DEFAULT: "+str(default)+"\n"
                show_help += f"""    ALTERNATIVES: -{attribute}={attribute.upper()}, 
                                                   -{attribute}:{attribute.upper()}, 
                                                   -{attribute} {attribute.upper()}\n"""    
                show_help += "\n    [if a value for the variable isn't specified, then its default is used]"
                show_help += "\n\n optional arguments:"
                show_help += "    --h, --help\t\t\t\t[show this help message and exit] \n"
        return show_help

    # This method collects all attributes and passes them to the parser.
    def add_argument(self, attribute, var_type="str", default="", help_txt=""):
        self.attributes.append(attribute)
        self.var_types.append(var_type)
        self.defaults.append(default)
        self.help_txts.append(help_txt)
        self.data[attribute] = []

    # This method detects values with units within the message. For example, "temperature = 38 degrees"
    def find_unit_value(self, message, variable, unit, default=0, help_txt="Specify variable and unit of measure"):
        # Attempt to find int values.
        self.add_argument(variable, int, 0, help_txt)
        self.add_argument(unit, int, 0, help_txt)
        detected_variable_int = self.parse(message)[variable]
        detected_unit_int = self.parse(message, reverse=True)[unit]

        # Attempt to find float values.
        self.add_argument(variable, float, 0, help_txt)
        self.add_argument(unit, float, 0, help_txt)
        detected_variable_float = self.parse(message)[variable]
        detected_unit_float = self.parse(message, reverse=True)[unit]
        
        # Find the common, most probable value for the attribute specified. 
        union = list(set(detected_variable_int).union(detected_unit_int, detected_variable_float, detected_unit_float))
        try: return [x for x in union if x != 0][0]
        except: return default
    
    # This method collects all values within the message, sorts and returns them as a single list.
    def sorted_values(self):
        sentence = []
        loc = []
        try: # Only perform this if there are atributes specified within the string. 
            for attribute in self.attributes:
                for i in self.parse(self.message)[attribute]: 
                    sentence.append(i)
                    try: loc.append(self.message.index(i))
                    except: loc.append(self.message.index(attribute))
            loc, sentence = map(list, zip(*sorted(zip(loc, sentence), reverse=False)))
        except: pass
        return sentence
    
    # This method strips all attributes and values to display the remaining string. 
    def remove_all_attributes(self):
        sentence = self.message
        sentence = sentence.replace("=", " ")
        sentence = sentence.replace("-", " ")
        sentence = sentence.replace(":", " ")
        sentence = sentence.replace(".", "")
        sentence = sentence.replace("'", "")
        sentence = sentence.replace('"', "")
        sentence = sentence.replace(",", "")
        
        stopwords = [item for attribute in self.attributes for item in self.data[attribute]] + self.attributes        
        try:
            for word in stopwords: 
                sentence = sentence.replace(str(int(word)), "") # Converts float to int variable, then to string. 
        except: 
            for word in stopwords: 
                sentence = sentence.replace(str(word), "") # Converts int to string. 
        return sentence.lstrip(" ").rstrip(" ") # Removes all spaces from the left and right of the string.

    # This method only retrieves attributes that were detected in the message, excluding all default values given.
    def show_message_attributes(self):
        return self.retrieved_attributes

'''TEST USAGE:'''
if __name__ == "__main__":
    # The test message you wish to process.
    message = '''I have two variables: -mass: 12 --vel= OR [this is just another descriptor, apple pie] 
    AND that new thing NOT apple strudel OR that new fangled thing SYN complicated NOT apple, orange, pear ice cream'''

    # Create a parser object. "True" if you wish to suppress help message from being displayed. 
    query = comparse(True)
    print(query)
    
    # Tell the parser what arguments it should accept.
    query.add_argument("vel", int, 10, "this is your velocity attribute")
    query.add_argument("mass", float, 10, "this is your mass attribute")
    query.add_argument("OR", str, "", "OR boolean operator")
    query.add_argument("AND", str, "", "AND boolean operator")
    query.add_argument("NOT", str, "", "NOT boolean operator")
    query.add_argument("SYN", str, "", "SYN method-call")

    # Give the parser a specific message for which it should extract arguments.
    print(f"This is the parsed message:\n{query.parse(message)}\n")
    print(f"These are the sorted values:\n{query.sorted_values()}\n")
    print(f"After attribute-value pairs have been removed:\n{query.remove_all_attributes()}\n")

    # Detect a value with a unit of measure within a message.
    message2 = 'The temperature in this room is too cold, crank it up to 27.6 degrees please.'
    print(f"Temperature = {query.find_unit_value(message2, 'temperature', 'degree')} degrees\n")

    # Detect single character attributes.
    message3 = "d10+5 + 1 d 20 for parried attack + 4d12 to smite + 1d10"
    query.add_argument("d", int, 20, "XdY+n")
    print(f"These are the set of D&D dice to roll: {query.parse(message3)['d']}")
    print(f"Conversely, these are the number of dice to roll: {query.parse(message3, reverse=True)['d']}")
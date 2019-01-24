'''COMPARSE - JUST LIKE ARGPARSE, ONLY BETTER!
Comparse is a flexible commandline parsing module. Designed to pick out ATTRIBUTES and assign VALUES to them from a message containing many un-formatted attributes/variables.
- message: the actual message,
- attribute: the actual attribute (variable) you wish to extract from the message,
- var_type: variable type, this accepts integers, string, float variables,
- default: the default value of the attribute,
- help_txt: the help text you wish to display,
- suppress_help_txt: if True, help_txt will not be displayed, 
- NOTE: the entire substring following an attribute marker will be parsed. This function outputs a a dictionary containing LISTS.
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
        #Shows the help text if the user requests it.
        if(("-h" or "-help") in message or message.endswith("-h")):
            help_list = [attribute for attribute in self.attributes if attribute in message] #Prepare only requested help text. 
            if not help_list: help_list = self.attributes #If no specific help requested, prepare them all!
            if not self.suppress_help_txt:
                return comparse.show_help(self, help_list)

        #Remove unwanted symbols (e.g. "=", ":", "[]", "()", "{}", etc.)
        message = message.replace("=", " ")
        message = message.replace(":", " ")
        #message = message.replace(".", "")
        message = message.replace("'", "")
        message = message.replace('"', "")
        message = message.replace("[", '')
        message = message.replace("]", '')
        message = message.replace("(", '')
        message = message.replace(")", '')
        message = message.replace("{", '')
        message = message.replace("}", '')
        self.message = message

        #Insert quotation marks after string attributes. This will ensure that the entire substring following an attribute marker is correctly parsed. #This function matches the entire attribute found in the sentence so that quotation marks can be applied accurately to the string.
        def attribute_match(string, match):
            for word in string.split():
                if match in word: return word
        
        #This returns a SET of attributes (it filters out duplicates and empty values).
        attributes = []
        for attribute in self.attributes: 
            attributes.append(attribute_match(message, attribute))
            attributes = list(set(attributes))
            attributes = [x for x in attributes if x is not None]

        #This applies the quotation marks to the string input. 
        for attribute in attributes:
            modified_attribute = ' '+attribute+' '
            message = modified_attribute.join('"{}"'.format(s.strip()) for s in message.split(attribute))
            if attributes.index(attribute)>0: message = message[1:-1]
        
        #This is the main engine that detects variables within the natural language text and populates them with values.
        args = shlex.split(message) #This splits the message. 
        
        #This section declares 'temp_options' and 'options' dictionaries and populates them.
        temp_options = {}
        options = {}
        for k,v in zip(args, args[1:]): 
            k = k.strip('-')
            temp_options[k] = []
        
        #This populates the 'temp_options' dictionary.
        for k,v in zip(args, args[1:]): 
            k = k.strip('-')
            for item in [x.strip(' ') for x in v.split(",")]: temp_options[k].append(item) #Split elements by comma.
            temp_options[k] = [x for x in temp_options[k] if x] #Get rid of empty elements from the list.

        #This picks out only attributes specified in the message and populates the other, unspecified attributes with default values. 
        for attribute in self.attributes: 
            if attribute in list(temp_options.keys()): options[attribute] = temp_options[attribute]
            else: options[attribute] = [self.defaults[self.attributes.index(attribute)]]

        #This section declares 'data' dictionary and populates it.
        self.data = {}
        for attribute in self.attributes: self.data[attribute] = []
        
        #This applies the correct variable type to the individual variables.
        for attribute, var_type, default in zip(self.attributes, self.var_types, self.defaults):
            if (var_type == "int"):
                for element in options[attribute]: 
                    try: self.data[attribute].append(int(element))
                    except:
                        self.data[attribute].append(int(default))
            if (var_type == "str"):
                #Initially strips white-spaces and splits the string by commas. Appends the default value if none are specified. This is a rigorous algorithm which appends default values even if values have been partially specified by the user.
                for element in options[attribute]: 
                    try: 
                        for item in [x.strip() for x in element.split(',')]: self.data[attribute].append(str(item))   
                    except: 
                        if default:
                            for item in [x.strip() for x in default.split(',')]: self.data[attribute].append(str(item))  
                        else: self.data[attribute].append(str(default))  
            if (var_type == "float"):
                for element in options[attribute]: 
                    try: self.data[attribute].append(float(element))   #Updates if "attribute" exists, else adds "attribute".
                    except: self.data[attribute].append(float(default))
            if (var_type == "bool"):
                for element in options[attribute]: 
                    try: 
                        if element.lower() == 'false': self.data[attribute].append(bool(0))
                        if element.lower() == 'true': self.data[attribute].append(bool(1))
                    except: self.data[attribute].append(bool(default))
    
        return self.data
    
    #This method shows the formatted help text. Note that the printed text may be different from that which is returned by the method. Allows for greater flexibility.
    def show_help(self, help_list):
        show_help = "" #Text variable to be returned.
        '''
        #Optional print statements which could be used:
        print("\nCommand parsing for this program was done using COMPARSE: a flexible command-line parsing module. Designed to extract ATTRIBUTES and assign VALUES to them from a message containing many un-formatted attributes/variables.")
        print("\n usage:\n")
        for attribute, help_txt, var_type in zip(self.attributes, self.help_txts, self.var_types):
            if attribute in help_list:
                print(attribute)
                print("    "+help_txt)
                print("    VARIABLE TYPE: "+var_type)
                print("    ALTERNATIVES: "+ "-"+attribute+"="+str(attribute).upper() + ", -"+attribute+":"+str(attribute).upper() + ", -"+attribute+" "+str(attribute).upper() + "\n")
                print("    [if the value for the variable is not specified, then its specified default value is used]")
                print("\n optional arguments:")
                print("    --h, --help\t\t\t\t[show this help message and exit] \n")
        '''
        #Collate help text into a neat variable to be returned by the method.
        show_help += "\nCommand parsing for this program was done using COMPARSE: a flexible commandline parsing module. Designed to pick out ATTRIBUTES and assign VALUES to them from a message containing many un-formatted attributes/variables."
        show_help += "\n\n usage:\n"
        for attribute, help_txt, var_type in zip(self.attributes, self.help_txts, self.var_types):
            #Only show requested help, don't bombard the user with everything!
            if attribute in help_list:
                show_help += "\n"+attribute
                show_help += "\n    "+help_txt+"\n"
                show_help += "    VARIABLE TYPE: "+var_type+"\n"
                show_help += "    ALTERNATIVES: "+ "-"+attribute+"="+str(attribute).upper() + ", -"+attribute+":"+str(attribute).upper() + ", -"+attribute+" "+str(attribute).upper() + "\n"
                show_help += "\n    [if the value for the variable is not specified, then its specified default value is used]"
                show_help += "\n\n optional arguments:"
                show_help += "    --h, --help\t\t\t\t[show this help message and exit] \n"
        return show_help

    #This method collects all attributes from the "outside world" into arrays and passes them into the parse function within the local environment.
    def add_argument(self, attribute, var_type="str", default="", help_txt=""):
        self.attributes.append(attribute)
        self.var_types.append(var_type)
        self.defaults.append(default)
        self.help_txts.append(help_txt)
        self.data[attribute] = []
    
    #This method collects all values within the message, sorts and returns them as a single list.
    def sorted_values(self):
        sentence = []
        loc = []
        try: #Only perform this if there are atributes specified within the string. 
            for attribute in self.attributes:
                for i in self.parse(self.message)[attribute]: 
                    sentence.append(i)
                    try: loc.append(self.message.index(i))
                    except: loc.append(self.message.index(attribute))
            loc, sentence = map(list, zip(*sorted(zip(loc, sentence), reverse=False)))
        except: pass
        return sentence
    
    #This method strips all attributes and values to display the remaining string. 
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
            for word in stopwords: sentence = sentence.replace(str(int(word)), "") #Converts float to int variable, then to string. 
        except: 
            for word in stopwords: sentence = sentence.replace(str(word), "") #Converts int to string. 
        return sentence

'''USAGE:
#The test message you wish to process.
message = 'I have two variables: -mass: 12 --vel= OR [this is just another descriptor, apple pie] AND that new thing NOT apple strudel OR that new fangled thing SYN complicated NOT apple, orange, pear ice cream'
#message = "-mass 12 -h"

#Create a parser object. "True" if you wish to suppress help message from being displayed. 
query = comparse(True)

#Tell the parser what arguments it should accept.
query.add_argument("vel", "int", 10, "this is your velocity attribute")
query.add_argument("mass", "float", 10, "this is your mass attribute")
query.add_argument("OR", "str", "", "OR boolean operator")
query.add_argument("AND", "str", "", "AND boolean operator")
query.add_argument("NOT", "str", "", "NOT boolean operator")
query.add_argument("SYN", "str", "", "SYN method-call")

#Give the parser a specific message for which it should extract arguments.
print(query.parse(message))
print(query.sorted_values())
print(query.remove_all_attributes())
'''
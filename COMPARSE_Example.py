from comparse import comparse
query = comparse(False)
query.add_argument("!log_this_channel", "str", "logs.txt", "Logs the channel the administrator is currently in to a specified file. Note, only administrators may use this. USAGE: !log_this_channel='logs.txt' See below for options.")
query.add_argument("content_filter", "str", None, " + OPTION: Filter log by content. USAGE: !log_this_channel, content_filter=None")
query.add_argument("exclude_content", "str", None, " + OPTION: Exclude content from log. USAGE: !log_this_channel, exclude_content=None")
query.add_argument("log_attachments", "bool", True, " + OPTION: Logs attachments. USAGE: !log_this_channel, log_attachments=True")
query.add_argument("log_author", "bool", False, " + OPTION: Logs author of message. USAGE: !log_this_channel, log_author=False")
query.add_argument("!print_to_channel", "str", None, "Print the message attachments to the channel the administrator is currently in. Note, only administrators may use this. USAGE: !print_to_channel")
query.add_argument("!profanity_filter", "bool", True, "Toggles the profanity filter on or off (filter swear words). Note, only administrators may use this. USAGE: !profanity_filter=False")

#FIRST EXAMPLE
message = "This message will print out the help text for: !log_this_channel -h, regradless of the sentence structure."
file_name = query.parse(message)
try: print(file_name['exclude_content'][0])
except: print(query.parse(message))

#SECOND EXAMPLE
message = "!log_this_channel=example.txt, content_filter=posted, log_attachments=False, log_author=False, exclude_content='apple, pear, orange'"
file_name = query.parse(message)
try: print(file_name)
except: print(query.parse("--help"))

#THIRD EXAMPLE
message = "!log_this_channel, exclude_content='apple, pear'"
file_name = query.parse(message)
try: print(file_name['exclude_content'])
except: print(query.parse("--help"))

#FOURTH EXAMPLE
message = "i made a booboo !log_this_channel, log_author=False, log_attachments=False"
file_name = query.parse(message)
try: print(file_name)
except: print(query.parse(message))
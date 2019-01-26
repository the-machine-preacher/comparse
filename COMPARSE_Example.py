from comparse import comparse
query = comparse(False)
query.add_argument("!log_this_channel", str, "logs.txt", "Logs the channel the administrator is currently in to a specified file. Note, only administrators may use this. USAGE: !log_this_channel='logs.txt' See below for options.")
query.add_argument("content_filter", str, None, " + OPTION: Filter log by content. USAGE: !log_this_channel, content_filter=None")
query.add_argument("exclude_content", str, None, " + OPTION: Exclude content from log. USAGE: !log_this_channel, exclude_content=None")
query.add_argument("log_attachments", bool, True, " + OPTION: Logs attachments. USAGE: !log_this_channel, log_attachments=True")
query.add_argument("log_author", bool, False, " + OPTION: Logs author of message. USAGE: l!og_this_channel, log_author=False")
query.add_argument("!print_to_channel", str, None, "Print the message attachments to the channel the administrator is currently in. Note, only administrators may use this. USAGE: !print_to_channel")
query.add_argument("!profanity_filter", bool, False, "Toggles the profanity filter on or off (filter swear words). Note, only administrators may use this. USAGE: !profanity_filter=False")
query.add_argument("!int_variable", int, 13, "This is a random interger variable.")

#FIRST EXAMPLE
message = "This message will print out the help text for: !log_this_channel -h, regradless of the sentence structure."
file_name = query.parse(message)
try: print(file_name['exclude_content'][0])
except: print(query.parse(message))

#SECOND EXAMPLE
message = "!log_this_channel=example.txt, content_filter=posted, log_attachments=false, log_author=FALSE, exclude_content='apple, pear, orange', !int_variable=26"
file_name = query.parse(message)
try: 
    print(file_name)
    print(query.error_log)
except: print(query.error_log)

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

#FIFTH EXAMPLE (extract variables from COMPARSE)
message = "!log_this_channel=example.txt, content_filter=posted, log_attachments=false, log_author=false, exclude_content='apple, pear, orange', !int_variable=26"
message = "!log_this_channel, log_author true"
file_name = query.parse(message)["!log_this_channel"][0] #Specify a name for the log file.
content_filter = query.parse(message)["content_filter"][0]
log_attachments = query.parse(message)["log_attachments"][0]
log_author = query.parse(message)["log_author"][0]
exclude_content = query.parse(message)["exclude_content"]
print(query.parse(message))
print(file_name, content_filter, log_attachments, log_author, exclude_content)
from comparse import comparse
query = comparse(False)
query.add_argument("log_channel", "str", "logs.txt", "Logs the channel in specified file. DEFAULT ARGUMENT(S): log_channel='logs.txt'")
query.add_argument("content_filter", "str", "None", "Filter log by content. DEFAULT ARGUMENT(S): content_filter='None'")
query.add_argument("log_attachments", "bool", True, "Logs attachments. DEFAULT ARGUMENT(S): log_attachments=True")
query.add_argument("log_author", "bool", False, "Logs author of message. DEFAULT ARGUMENT(S): log_author=False")
query.add_argument("exclude_content", "str", "None", "Exclude content from log. DEFAULT ARGUMENT(S): exclude_content='None'")

#FIRST EXAMPLE
message = "log_channel --h"
file_name = query.parse(message)
try: print(file_name['exclude_content'][0])
except: print(query.parse("--help"))

#SECOND EXAMPLE
message = "log_channel=example.txt, content_filter=posted, log_attachments=True, log_author=True, exclude_content='apple, pear, orange'"
file_name = query.parse(message)
try: print(file_name)
except: print(query.parse("--help"))

#THIRD EXAMPLE
message = "log_channel, exclude_content='apple, pear'"
file_name = query.parse(message)
try: print(file_name['exclude_content'])
except: print(query.parse("--help"))

#FOURTH EXAMPLE
message = "i made a booboo"
file_name = query.parse(message)
try: print(file_name['mistaken_content'][0])
except: print(query.parse("--help"))
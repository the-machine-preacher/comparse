from comparse import comparse
query = comparse(False)
query.add_argument("log_channel", "str", "logs.txt", "Logs the channel in specified file. DEFAULT ARGUMENT(S): log_channel 'logs.txt'")
query.add_argument("content_filter", "str", "Nuby", "Filter log by content. DEFAULT ARGUMENT(S): content_filter 'none'")
query.add_argument("log_attachments", "str", "Tuby", "Logs attachments. DEFAULT ARGUMENT(S): log_attachments 'True'")
query.add_argument("log_author", "str", "False", "Logs author of message. DEFAULT ARGUMENT(S): log_author=False")
query.add_argument("exclude_content", "str", "None", "Exclude content from log. DEFAULT ARGUMENT(S): exclude_content='None'")

#FIRST PROCESS
message = "log_channel --h"
file_name = query.parse(message)
try: print(file_name['exclude_content'][0])
except: print(query.parse("--help"))

#SECOND PROCESS
message = "log_channel=example.txt, content_filter=posted, log_attachments=True, log_author=True, exclude_content='apple, pear, orange'"
file_name = query.parse(message)
try: print(file_name['log_channel'])
except: print(query.parse("--help"))

#THIRD PROCESS
message = "log_channel, exclude_content='apple, pear'"
file_name = query.parse(message)
try: print(file_name['exclude_content'])
except: print(query.parse("--help"))

#FOURTH PROCESS
message = "i made a booboo"
file_name = query.parse(message)
try: print(file_name['mistaken_content'][0])
except: print(query.parse("--help"))
from comparse import comparse
query = comparse(False)
query.add_argument("log_channel", "str", "logs.txt", "Logs the channel in specified file. DEFAULT ARGUMENT(S): log_channel 'logs.txt'")
query.add_argument("content_filter", "str", "Nuby", "Filter log by content. DEFAULT ARGUMENT(S): content_filter 'none'")
query.add_argument("log_attachments", "str", "Tuby", "Logs attachments. DEFAULT ARGUMENT(S): log_attachments 'True'")
query.add_argument("log_author", "str", "False", "Logs author of message. DEFAULT ARGUMENT(S): log_author=False")
query.add_argument("exclude_content", "str", "None", "Exclude content from log. DEFAULT ARGUMENT(S): exclude_content='None'")

'''
#FIRST PROCESS
message = "log_channel --h"
try:
    file_name = query.parse(message)
    print(file_name)
except: pass
'''
#SECOND PROCESS
message = "log_channel=example.txt, content_filter=posted, log_attachments=True, log_author=True, exclude_content='apple, pear, orange'"
try:
    file_name = query.parse(message)
    print(file_name)
except: pass

#THIRD PROCESS
try:
    message = "log_channel, exclude_content='apple, pear'"
    file_name = query.parse(message)
    print(file_name)
except: pass

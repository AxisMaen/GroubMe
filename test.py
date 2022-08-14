import dataHelper
import dataRetrieval

#37055818 = main chat
#60699437 = monke chat

print(dataRetrieval.getAPIGroups())

#these might take several minutes each depending on the # of messages in the group
'''
print("--- Running searchMessages ---")
for message in dataHelper.searchMessages("60699437", "monke"):
    print(message["name"] + ": " + message["text"])
'''
'''
print("--- Running getGroupStats ---")
for member in dataHelper.getGroupStats("60699437"):
    print(member)
'''
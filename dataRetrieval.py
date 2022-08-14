import requests
import dataHelper
import json

'''
This module is responsible for gathering data from either the API or from
local files.
'''

'''
Current plan is to have these functions support both getting data from the api
and local data from a download

Need to implement supporting local json reading (streaming using ijson library)

Might want to use the class for chatMessages here to support storing message
data more easily
'''

baseEndpoint = "https://api.groupme.com/v3"

clientId = "4y3lFZ9DhxlgXX88VoQImZ9cLN9YK7u2YpocK6Jst9fCMoxn"

#getting the access token from a file so it is not public on Git
#in the future we will have user input their own access token on UI
accessToken = ""
with open('Files\\Access Token.txt') as f:
    accessToken = f.read()

'''
Returns a json response from the given endpoint
Returns False on error
'''
def doAPIRequest(endpoint):
    try:
        #call the API
        response = requests.get(url=endpoint)
        response.raise_for_status()

        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        #on any error, return False
        print(e)
        return False

'''
Returns a list of tuples of all members in the group (userId, username)
'''
def getAPIGroupMembers(groupId):
    endpoint = baseEndpoint + "/groups/" + groupId + "?token=" + accessToken

    response = doAPIRequest(endpoint)
    
    members = []
    for member in response["members"]:
        members.append((member["user_id"], member["nickname"]))

    return members

'''
Gets all of the user's active groups
Returns a list of json responses for all active groups
'''
def getAPIGroups():

    #responses are pagenated, potentially need multiple requests to get all groups

    groups = [] #list of json responses
    pageNum = 1

    while True:

        endpoint = baseEndpoint + "/groups?&per_page=30&omit=memberships&page=" + str(pageNum) + "&token=" + accessToken

        response = doAPIRequest(endpoint)

        #if the response is empty, we have gotten every group or an error
        if(not response):
            return groups

        groups.extend(response)
        pageNum += 1


'''
Gets a chunk of messages from a group, messages are retrieved from newest to oldest
groupId - (string) ID of the group to get messages from
beforeId - (string) Message ID, get the messages before the given message ID (optional)
Returns a list of json responses for messages, empty list if no messages are retrieved
'''
def getAPIMessageChunk(groupId, beforeId=None):
    limit = 100 #how many messages to get in one request (max 100)

    endpoint = baseEndpoint + "/groups/" + groupId + "/messages?limit=100" 

    #if a beforeId is provided, include it in the request
    if(beforeId):
        endpoint += "&before_id=" + beforeId
        
    endpoint += "&token=" + accessToken

    response = doAPIRequest(endpoint)
    if(not response):
        return []

    return response["messages"]

'''
The "chunk" is all the group's message data, could potentially use a lot of memory
Should eventually find some way to stream the data in for less memory usage if it is
a problem.

Returns a list of json responses
'''
def getLocalMessageChunk(groupId):
    with open(str(groupId) + "/message.json", encoding = 'UTF-8') as json_file:
        print("Loading messages")
        return json.load(json_file)

'''
Returns a list of tuples of all members in the group (userId, username)
'''
def getLocalGroupMembers():
    return "Implement here"

'''
Identify which groups are downloaded locally
'''
#need to find how to format the return, I don't think a group json response comes with
#locally downloaded data
def getLocalGroups():
    return None
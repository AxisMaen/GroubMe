import requests

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
def doRequest(endpoint):
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
def getGroupMembers(groupId):
    endpoint = baseEndpoint + "/groups/" + groupId + "?token=" + accessToken

    response = doRequest(endpoint)
    
    members = []
    for member in response["members"]:
        members.append((member["user_id"], member["nickname"]))

    return members

'''
Gets all of the user's active groups
Returns a list of json responses for all active groups
'''
def getGroups():

    #responses are pagenated, potentially need multiple requests to get all groups

    groups = [] #list of json responses
    pageNum = 1

    while True:

        endpoint = baseEndpoint + "/groups?&per_page=30&omit=memberships&page=" + str(pageNum) + "&token=" + accessToken

        response = doRequest(endpoint)

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
def getMessageChunk(groupId, beforeId=None):
    limit = 100 #how many messages to get in one request (max 100)

    endpoint = baseEndpoint + "/groups/" + groupId + "/messages?limit=100" 

    #if a beforeId is provided, include it in the request
    if(beforeId):
        endpoint += "&before_id=" + beforeId
        
    endpoint += "&token=" + accessToken

    response = doRequest(endpoint)
    if(not response):
        return []

    return response["messages"]
import dataRetrieval
import user

'''
We only want to pass through a group one time, so we should get all stats in one go
Tracks the following stats: messages per user, likes per user, like:message ratio per user,
most liked message(s)


could save stats to a file of some sort, user can refresh when desired
'''
def getGroupStats(groupId, local=False):
    
    #list of json responses for a message
    messageChunk = []

    #dict where key is userId and the value is the User object
    #will eventually include all members who have chatted (including ones who have left)
    memberDict = {} 

    ### Initial data retrieval from api/local ###
    if(local):
        messageChunk = dataRetrieval.getLocalMessageChunk(groupId)
        members = dataRetrieval.getLocalGroupMembers(groupId)
    #return an error if we do not have the given group locally
    else:
        messageChunk = dataRetrieval.getAPIMessageChunk(groupId)
        members = dataRetrieval.getGroupMembers(groupId) #(userId, username), does not include left members
        for member in members:
            memberDict[member[0]] = user.User(groupId, member[0], member[1])
    

    #used in finding the most liked message(s)
    maxLikes = 0
    maxMessages = [] #list of messages in json form

    ### Begin iterating through all messages ###
    while(messageChunk):
        for message in messageChunk:

            messageId = message["id"]
            userId = message["user_id"]
            username = message["name"]
            likes = len(message["favorited_by"])

            #if message is from someone who is no longer in the group, make sure to add them
            if(userId not in memberDict.keys()):
                memberDict[userId] = user.User(groupId, userId, "Inactive User (" + username + ")")

            ### messages per user ###
            memberDict[userId].messageCount += 1
            
            ### likes per user ###
            memberDict[userId].likeCount += likes

            ### most liked message(s) ###
            if(likes == maxLikes):
                maxMessages.append(message)
            elif(likes > maxLikes):
                maxMessages = [message]
                maxLikes = likes
        
        #getting the next message chunk
        if(local):
            #the local chunk contained everything, so we are done
            messageChunk = []
        else:
            messageChunk = dataRetrieval.getAPIMessageChunk(groupId, messageId)

    ##### POST PROCESSING (after all messages are read) #####

    ### like message ratio ###
    for member in memberDict.values():
        member.likeMessageRatio = round(member.likeCount/member.messageCount, 3)

    return memberDict.values()



### NEEDS REWORKING ###
def searchMessages(groupId, searchPhrase, local=False):
    
    messageChunk = []
    if(local):
        messageChunk = dataRetrieval.getLocalMessageChunk(groupId)
    else:
        messageChunk = dataRetrieval.getAPIMessageChunk(groupId)
    
    foundMessages = []
    while(messageChunk):
        for message in messageChunk:
            
            messageId = message["id"]
            if(searchPhrase.lower() in str(message["text"]).lower()):
                foundMessages.append(message)
        
        #getting the next message chunk
        if(local):
            #the local chunk contained everything, so we are done
            messageChunk = []
        else:
            messageChunk = dataRetrieval.getAPIMessageChunk(groupId, messageId)

    return foundMessages[::-1]
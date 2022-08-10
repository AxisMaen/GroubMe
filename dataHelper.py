import api
import user

'''
Current plan is to have these functions support both getting data from the api
and local data from a download

Need to implement supporting local json reading (streaming using ijson library)

Might want to use the class for chatMessages here to support storing message
data more easily
'''

'''
Searches a group for all messages containing the given search phrase (case insensitive)
Returns a list of json responses for messages that contain the search phrase
Returned messages are in chronological order from oldest to newest
'''
def searchMessages(groupId, searchPhrase):
    
    messageChunk = api.getMessageChunk(groupId)
    
    foundMessages = []
    while(messageChunk):
        for message in messageChunk:
            
            messageId = message["id"]
            if(searchPhrase.lower() in str(message["text"]).lower()):
                foundMessages.append(message)
        
        messageChunk = api.getMessageChunk(groupId, messageId)

    return foundMessages[::-1]


'''
We only want to pass through a group one time, so we should get all stats in one go
Tracks the following stats: messages per user, likes per user, like:message ratio per user,
most liked message(s)


could save stats to a file of some sort, user can refresh when desired
'''
def getGroupStats(groupId):
    messageChunk = api.getMessageChunk(groupId)

    members = api.getGroupMembers(groupId) #(userId, username), does not include left members

    #dict where key is userId and the value is the User object
    #will eventually include all members who have chatted (including ones who have left)
    memberDict = {}
    for member in members:
        memberDict[member[0]] = user.User(groupId, member[0], member[1])

    #used in finding the most liked message(s)
    maxLikes = 0
    maxMessages = [] #list of messages in json form

    while(messageChunk):
        for message in messageChunk:
            messageId = message["id"]
            userId = message["user_id"]
            username = message["name"]
            likes = len(message["favorited_by"])

            #if message is from someone who is no longer in the group, make sure to add them
            if(userId not in memberDict.keys()):
                memberDict[userId] = user.User(groupId, userId, "Left User (" + username + ")")

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

        messageChunk = api.getMessageChunk(groupId, messageId)

    ##### POST PROCESSING (after all messages are read) #####

    ### like message ratio ###
    for member in memberDict.values():
        member.likeMessageRatio = round(member.likeCount/member.messageCount, 3)

    return memberDict.values()
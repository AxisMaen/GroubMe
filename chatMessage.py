from email import message
import json

class ChatMessage:

    '''
    attachments
        source_url
        type
        url
    
    avatar_url
    created_at
    group_id
    id
    name (nickname of sender)
    sender_id
    sender_type
    source_guid (idk what this is)
    system (bool)
    text
    user_id (same as sender_id??)
    platform

    '''

    def __init__(self, message):
        self.text = str(message["text"])
        self.likes = int(len(message["favorited_by"]))
        self.senderName = str(message["name"]) #nickname of the sender
        self.senderId = str(message["sender_id"])
        self.groupId = str(message["group_id"])
        self.isSystem = bool(message["system"])
        self.timestamp = float(message["created_at"])

        self.imageURLs = []
        self.videoURLs = []
        for attachment in message["attachments"]:
            if(str(attachment["type"]) == "image" and "url" in attachment.keys()):
                self.imageURLs.append(str(attachment["url"]))
            if(str(attachment["type"]) == "video" and "url" in attachment.keys()):
                self.videoURLs.append(str(attachment["url"]))

    #returns true if message has images or videos, false otherwise    
    #def hasAttachedMedia(self):

    #returns true if message mentions at lease one user, false otherwise
    #def hasMention(self):

    #returns the text of the message plus any attachment urls
    def getFullMessage(self):
        messageText = self.senderName + ": " + self.text

        if(self.imageURLs or self.videoURLs):
            messageText += "\n Attachments: "
        for imageURL in self.imageURLs:
            messageText += imageURL + "\n"
        for videoURL in self.videoURLs:
            messageText += videoURL + "\n"

        return messageText

    

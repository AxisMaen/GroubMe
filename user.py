class User:

    '''
    Used to track the stats of a user in a specfic group
    Will likely write all attributes to a file or similar
    '''

    def __init__(self, groupId, userId, name):
        self.groupId = groupId
        self.userId = userId
        self.name = name
        self.messageCount = 0
        self.likeCount = 0
        self.likeMessageRatio = 0

    def __str__(self):
        return self.name + "\nMessages: " + str(self.messageCount) + "\nLikes: " + str(self.likeCount) + "\nRatio: " + str(self.likeMessageRatio)
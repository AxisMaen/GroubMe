# GroubMe

Pulling GroupMe chat data from GroupMe's API and doing fun things with it.

Eventually will also support pre-downloaded local data and a nice UI. Want to make a web app but it takes a while to pull every message from big chats so I'll do some thinking.

You'll need your GroupMe access token to use for now. Go to the API documentation and log in. Then click "access token" and copy it. Paste it into the AccessToken.txt found in the Files folder. To get data from a certain group, you will need the group ID. You can get this by running getGroups() and going through the response to get the IDs for all of your active groups (see test.py).

If you're interesting in modifying to get specific data, here is the API documentation.
https://dev.groupme.com/docs/v3
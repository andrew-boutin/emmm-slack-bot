# Script to get Bot ID
# Modified script from this source: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
# Requires BOT_NAME & SLACK_BOT_TOKEN environment variables
# Linux
import os
from slackclient import SlackClient


BOT_NAME = os.environ.get('SLACK_BOT_NAME')
BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

if not BOT_NAME:
    print("Missing env variable BOT_NAME.")

if not BOT_TOKEN:
    print("Missing env variable BOT_TOKEN.")

print("Using BOT_NAME: {}, BOT_TOKEN: {}.".format(BOT_NAME, BOT_TOKEN))
print("Attempting to determine BOT_ID.")

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
api_call = slack_client.api_call("users.list")

found = False


if api_call.get('ok'):
    # retrieve all users so we can find our bot
    users = api_call.get('members')

    for user in users:
        if 'name' in user and user.get('name') == BOT_NAME:
            found = True
            print("Bot ID: {}.".format(user.get('id')))

    if not found:
        print("Could not find bot user with the name " + BOT_NAME)
else:
    print("Failed to make api call to Slack.")


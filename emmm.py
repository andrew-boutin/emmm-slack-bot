# EMMM SLACK BOT
# Author: andrew-boutin
import os
from slackclient import SlackClient

BOT_NAME = os.environ.get("SLACK_BOT_NAME")
BOT_ID = os.environ.get("SLACK_BOT_ID")
BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

if not BOT_NAME or not BOT_ID or not BOT_TOKEN:
    print("Env vars BOT_NAME, BOT_ID, & BOT_TOKEN are required.")
    sys.exit(-1)

slack_client = SlackClient(BOT_TOKEN)

if not slack_client.rtm_connect():
    print("Connection to Slack failed.")
    sys.exit(-1)

print("Connected to Slack.")


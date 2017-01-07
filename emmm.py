"""EMMM Slack Bot

Slack Bot that can randomly choose a user from the channel when prompted.

Author: andrew-boutin

Terminology:
- Response: Data read from Slack - can contain 0 to n messages..
- Message:  Data subsets from Slack responses that represent different types of messages.

Credits:
Used this source to get started: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
"""
import os
import time
import random
from slackclient import SlackClient


class EMMM_Slack_Bot():
    """Slack Bot that can randomly choose a user from a channel when mentioned."""

    def __init__(self, bot_name, bot_id, bot_token, known_bot_names=[]):
        """"""
        self.text_key = 'text'
        self.channel_key = 'channel'
        self.type_key = 'type' # Responses have a type which designates what fields they should have
        self.message_key = 'message'
        self.channel_key = 'channel'
        self.members_key = 'members'
        self.user_key = 'user'
        self.id_key = 'id'
        self.name_key = 'name'

        self.BOT_NAME = bot_name
        self.BOT_ID = bot_id
        self.BOT_TOKEN = bot_token

        if not self.BOT_NAME or not self.BOT_ID or not self.BOT_TOKEN:
            raise Exception("Env vars BOT_NAME, BOT_ID, & BOT_TOKEN are required.")

        self.slack_client = SlackClient(self.BOT_TOKEN)
        self.bot_mention_tag = '<@{}>'.format(self.BOT_ID)
        self.known_message_types = ['message', # Message sent from another user in a channel
                                    'hello', # Issued after bot connects
                                    'desktop_notification', # Sent to push a desktop notification if that setting is turned on for a user
                                    'user_typing', # Sent when a user starts typing in a channel
                                    'presence_change', # Sent when a user becomes active or goes inactive
                                    'reconnect_url', # Reconnection URL sent after connecting
                                   ]

        # Having a mapping of known user ids to names is useful
        self.user_id_name_dict = self.populate_id_name_dict()

        # Knowing who the bots are allows us to not consider them later
        self.known_bot_ids = self.lookup_bot_ids_by_names(known_bot_names)

        print("Bot initialized. Ready to connect.")

    def connect(self):
        """"""
        if not self.slack_client.rtm_connect():
            raise Exception("Connection to Slack failed.")

        print("Bot connected to Slack. Ready to start.")

    def start_bot(self):
        """"""
        while True:
            response = self.slack_client.rtm_read()

            messages = self.parse_response(response)

            for message in messages:
                if self.is_message_for_bot(message):
                    self.handle_message(message)

            time.sleep(1)

    def parse_response(self, response):
        """Parse the response from Slack for messages the bot may care about.

        A valid message should have the type, text, and channel it came from.
        [{'user': id, 'team': id, 'channel': id, 'text': '<@U3M4U1QUD> sup', 'ts':, 'type':}]
        """
        messages = []

        if not response or not len(response) > 0:
            return messages

        for message in response:
            # Messages must have a type or else the data format is unknown
            if self.type_key in message:
                msg_type = message[self.type_key]

                if msg_type not in self.known_message_types:
                    print("Unknown message type {}: {}".format(msg_type, message))
                    continue

                if msg_type == self.message_key:
                    if self.text_key in message and self.channel_key in message:
                        messages.append(message)

        return messages

    def is_message_for_bot(self, message):
        """Check if the message was directed at the bot.

        This means '@emmm ...
        """
        text = message[self.text_key]
        return text.startswith(self.bot_mention_tag)

    def handle_message(self, message):
        text = message[self.text_key]

        # TODO: For now all messages to the bot trigger emmm
        self.eeny_meeny_miny_moe(message)

    def eeny_meeny_miny_moe(self, message):
        """"""
        # Get list of all users in the channel
        users = self.get_users_in_channel(message[self.channel_key])

        # Remove any known bots lurking in the channel
        users = [user for user in users if user not in self.known_bot_ids]

        # Randomly pick a user
        index = random.randint(0, len(users) - 1)

        # Look up the username so it's human readable
        userid = users[index]

        if userid in self.user_id_name_dict:
            username = self.user_id_name_dict[userid]
        else:
            # Haven't encountered the userid before - look it up and cache it
            username = self.get_username_by_id(users[index])
            self.user_id_name_dict[userid] = username

        # Send message
        self.respond(username, message)

    def is_valid_command(self, valid_direct_bot_mention):
        """Check if the @emmm ... is a registered command."""
        raise Excepwtion("Not implemented.")

    def respond(self, output, message):
        """"""
        channel = message[self.channel_key]
        self.slack_client.api_call("chat.postMessage", channel=channel, text=output, as_user=True)

    def get_users_in_channel(self, channel):
        """Use channel ID."""
        channel_info = self.slack_client.api_call('channels.info', channel=channel)

        if channel_info and self.channel_key in channel_info:
            channel = channel_info[self.channel_key]

            if self.members_key in channel:
                members = channel[self.members_key]

                return members

        return []

    def get_username_by_id(self, userid):
        """"""
        info = self.slack_client.api_call('users.info', user=userid)

        if info and self.user_key in info:
            user = info[self.user_key]

            if self.name_key in user:
                return user[self.name_key]

        return ''

    def lookup_bot_ids_by_names(self, names):
        return [userid for userid in self.user_id_name_dict.keys() if self.user_id_name_dict[userid] in names]

    def populate_id_name_dict(self):
        members = self.get_all_users()
        return {member[self.id_key]: member[self.name_key] for member in members}

    def get_all_users(self):
        """"""
        data = self.slack_client.api_call('users.list')

        if data and self.members_key in data:
            members = data[self.members_key]
            return members

        return []


if __name__ == "__main__":
    # Gather the information necessary to connect the bot to Slack
    BOT_NAME = os.environ.get("SLACK_BOT_NAME")
    BOT_ID = os.environ.get("SLACK_BOT_ID")
    BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

    known_bot_names = ['pangolin', 'choboi']
    known_bot_names.append(BOT_NAME)

    # Connect and start listening
    emmm = EMMM_Slack_Bot(bot_name=BOT_NAME, bot_id=BOT_ID, bot_token=BOT_TOKEN, known_bot_names=known_bot_names)
    emmm.connect()
    emmm.start_bot()


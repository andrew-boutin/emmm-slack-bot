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
        """Initialize the Slack Bot.

        Set up variable information and create the Slack Client.

        Args:
            bot_name (String): Name of the Slack Bot.
            bot_token (String): Token configured for the Slack Bot.
            bot_id (String): ID of the Slack Bot.
        """
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
        self.known_message_types = ['message', # Message sent from another user in a channel
                                    'hello', # Issued after bot connects
                                    'desktop_notification', # Sent to push a desktop notification if that setting is turned on for a user
                                    'user_typing', # Sent when a user starts typing in a channel
                                    'presence_change', # Sent when a user becomes active or goes inactive
                                    'reconnect_url', # Reconnection URL sent after connecting
                                   ]

        # Text format of a user pinging our bot
        self.bot_mention_tag = '<@{}>'.format(self.BOT_ID)

        # Having a mapping of known user ids to names is useful
        self.user_id_name_dict = self.populate_id_name_dict()

        # Knowing who the bots are allows us to not consider them later
        self.known_bot_ids = self.lookup_known_ids_by_names(known_bot_names)

        print("Bot initialized. Ready to connect.")

    def connect(self):
        """Connect the Slack Client to Slack."""
        if not self.slack_client.rtm_connect():
            raise Exception("Connection to Slack failed.")

        print("Bot connected to Slack. Ready to start.")

    def start_bot(self):
        """Start having the Slack Bot listen for activity in Slack."""
        while True:
            response = self.slack_client.rtm_read()

            # Responses from Slack can contain multiple messages
            messages = self.parse_response(response)

            for message in messages:
                if self.is_message_for_bot(message):
                    self.handle_message(message)

            # Throttle the bot
            time.sleep(1)

    def parse_response(self, response):
        """Parse the response from Slack for messages sent from users.

        Args:
            response (JSON): Data sent from Slack that may contain messages.
        Return:
            [JSON]: List of messages sent from users.
        """
        messages = []

        if not response or not len(response) > 0:
            return messages

        for message in response:
            # Messages must have a type or else the data format is unknown
            if self.type_key in message:
                msg_type = message[self.type_key]

                # Log unknown message types so they can be investigated later
                if msg_type not in self.known_message_types:
                    print("Unknown message type {}: {}".format(msg_type, message))
                    continue

                # Check if the message is a user message
                if msg_type == self.message_key:
                    # Make sure it's well formed
                    if self.text_key in message and self.channel_key in message:
                        messages.append(message)

        return messages

    def is_message_for_bot(self, message):
        """Check if the message was directed at the bot (@emmm ...).

        Args:
            message (JSON): User message containing text.
        Return:
            bool: True if the text starts with a user mention for our bot.
        """
        text = message[self.text_key]
        return text.startswith(self.bot_mention_tag)

    def handle_message(self, message):
        """Determine how our bot should react to this message.

        Args:
            message (JSON): User message containing text.
        """
        text = message[self.text_key]

        # For now only a single emmm command
        self.eeny_meeny_miny_moe(message)

    def eeny_meeny_miny_moe(self, message):
        """Choose a user from the channel the message came from and respond with that user's name.

        Args:
            message (JSON): Message sent from the user.
        """
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

    def respond(self, output, message):
        """Send the given message to the channel that the original message came from.

        Args:
            message (JSON): Message that the user sent.
        """
        channel = message[self.channel_key]
        self.slack_client.api_call("chat.postMessage", channel=channel, text=output, as_user=True)

    def get_users_in_channel(self, channel):
        """Find a list of all the users in the given channel.

        Args:
            channel (JSON): Channel data to find users in.
        Return:
            [String]: List of user IDs from the input channel.
        """
        channel_info = self.slack_client.api_call('channels.info', channel=channel)

        if channel_info and self.channel_key in channel_info:
            channel = channel_info[self.channel_key]

            if self.members_key in channel:
                members = channel[self.members_key]

                return members

        return []

    def get_username_by_id(self, userid):
        """Retrive the text name of a user using their id.

        Args:
            userid (String): ID associated to the user's account.
        Return:
            String: Name of the user.
        """
        info = self.slack_client.api_call('users.info', user=userid)

        if info and self.user_key in info:
            user = info[self.user_key]

            if self.name_key in user:
                return user[self.name_key]

        return ''

    def lookup_known_ids_by_names(self, names):
        """Find the IDs for the given names based on previously collected user info.

        Args:
            names [String]: List of names to look up IDs for.
        Return:
            [String]: List of IDs associated to the input list of names.
        """
        return [userid for userid in self.user_id_name_dict.keys() if self.user_id_name_dict[userid] in names]

    def populate_id_name_dict(self):
        """Get a mapping of all users in Slack - ID to name.

        Return:
            [String:String]: Dictionary of user IDs with their corresponding names.
        """
        members = self.get_all_users()
        return {member[self.id_key]: member[self.name_key] for member in members}

    def get_all_users(self):
        """Retrieves a list of all the user data in Slack.

        Return:
            [JSON]: List of all user data from Slack.
        """
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

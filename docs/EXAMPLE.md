# Example

```bash
# Create a virtualenv for dependency isolation
python3 -m virtualenv env

# Activate the virtualenv
$ source env/bin/activate

# Install the dependencies
$ pip install -r requirements.txt

# Export environment variables required by the script
$ export SLACK_BOT_NAME=<redacted>
$ export SLACK_BOT_TOKEN=<redacted>

# Run the script to find the bot's ID
$ $ python get_bot_id.py
Using BOT_NAME: <redacted>, BOT_TOKEN: <redacted>.
Attempting to determine BOT_ID.
Bot ID: '<redacted>'

# Export the bot's ID as an environment variable
$ export SLACK_BOT_ID=<redacted>

# Start the Slack bot
$ python emmm.py
Bot initialized. Ready to connect.
Bot connected to Slack. Ready to start.
...
```

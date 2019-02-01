# EMMM Slack Bot

EMMM (Eeny, meeny, miny, moe) is a [Slack Bot](https://api.slack.com/bot-users) that can randomly choose a user in a channel out of all of the members in the channel.

![Eeny Meeny Miny Moe Gif](docs/emmm.gif)

## Use

Requires `python3`.

1. [Create a Slack Bot](https://api.slack.com/custom-integrations) in Slack itself. Choose a `name` and get the bot's API `token` from the *Integrations Section*.
1. Start the virtualenv, install dependencies, export environment variables, and retrieve the bot `ID` using `get_bot_id.py`.
1. Set the bot ID environment variable, and start up `emmm.py`.
1. In Slack, invite the bot to any of the channels that you want it available in.
1. @ mention the bot with `@emmm`.

See [EXAMPLE.md](docs/EXAMPLE.md) for more details on the scripting part outside of Slack itself.

## Details

You need the bot's `name`, `token`, and `id` to connect the bot to the *Slack APIs*.

The script `emmm.py` has all of the bot functionality.

```
# Using EMMM_Slack_Bot in emmm.py to start up eeny meeny miny moe
emmm = EMMM_Slack_Bot(bot_name=BOT_NAME, bot_id=BOT_ID, bot_token=BOT_TOKEN)
emmm.connect()
emmm.start_bot()
```

You can optionally pass in a list of bot names during initialization that you don't want to consider during the eeny meeny miny moe process.

```python
# Using EMMM_Slack_Bot in emmm.py to start the bot & not include other bots in responses
emmm = EMMM_Slack_Bot(bot_name=BOT_NAME, bot_id=BOT_ID, bot_token=BOT_TOKEN,
                      known_bot_names=['botname1', 'botname2', BOT_NAME])
...
```

While the bot's running in a channel, in Slack you can type **@emmm** to trigger the bot.

The bot will randomly choose a user out of all of the users in the channel, minus any bots configured to be ignored, and send a message to the channel with the user that was chosen.

---

Check out my [personal site](https://andrewboutin.com)!

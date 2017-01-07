# EMMM Slack Bot

EMMM is a [Slack Bot](https://api.slack.com/bot-users) that can randomly choose a user in a channel out of all of the members in the channel.

EMMM is short for [Eeny, meeny, miny moe](https://en.wikipedia.org/wiki/Eeny,_meeny,_miny,_moe).

---

### Setup

The bot uses `python3` with the `slackclient` package.

[Create a Slack Bot](https://api.slack.com/custom-integrations).

Choose a name and get the bot's `API Token` from the Integrations Section.

- TODO: helper script to get the bot id

### Use

You need the bot's `name`, `token`, and `id` to connect to Slack.

Here's the example on using the bot in the main function.

```
emmm = EMMM_Slack_Bot(bot_name=BOT_NAME, bot_id=BOT_ID, bot_token=BOT_TOKEN)
emmm.connect()
emmm.start_bot()
```

You can optionally pass in a list of bot names (`[String]`) to EMMM_Slack_Bot that you don't want to include in the choice process.

```
known_bot_names = ['bot1name', 'bot2name']
known_bot_names.append(BOT_NAME)

emmm = EMMM_Slack_Bot(bot_name=BOT_NAME, bot_id=BOT_ID, bot_token=BOT_TOKEN, known_bot_names=known_bot_names)
...
```

###### Author

Andy Boutin
www.andrewboutin.com

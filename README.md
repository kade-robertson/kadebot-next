# kadebot

A Telegram chat bot, built in Python.

# Development

1. Clone the repository.
2. Install the required dependencies:
   ```
   pip install python-telegram-bot ruamel.yaml requests omdb praw translate wikipedia wolframalpha
   ```
   You may need to run as `sudo` or with the `--user` flag if you don't have `sudo` priveledges.
3. Get a bot token for Telegram, through @BotFather.
4. Get your user ID for Telegram, through @myidbot.
5. Create a configuration file and configure the basic details:
   ```
   base:
     api_key: "Telegram bot token here"
     admins: [User ID here]
   ```
6. Configure each plugin's configuration as specified in their files.
7. Run the bot in one of two ways:
   ```
   ./kadebot.py --config file.conf
   python3 kadebot.py --config file.conf
   ```

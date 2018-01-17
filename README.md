# kadebot

A Telegram chat bot, built in Python.

# Configuration

The base set of configuration requires you to specify your Telegram bot token, any administrators (people you want to have access to /reload, /update, /kill), and you may disable any command, monitor, scheduled task, or even entire module you don't want to use. For example, your base section may look like this:
```
base:
  api_key: "notarealkey"
  admins:
    - 1234567890
    - 8888888888
  disabled:
    - t
    - randomaww
  disabled_monitors: []
  disabled_schedules: []
  disabled_modules:
    - SonnetGen
```
Configuration for individual commands can be seen in the command file itself, or refer to the `default.conf` to see what options are available.

# Development

1. Clone the repository.
2. Install the required dependencies:
   ```
   pip install python-telegram-bot ruamel.yaml requests omdb praw translate wikipedia wolframalpha markovify openweathermapy
   ```
   You may need to run as `sudo` or with the `--user` flag if you don't have `sudo` priveledges. You will also need [populartimes](https://github.com/m-wrzr/populartimes) which is not available on PyPi if you plan on setting up /popular. You may be able to omit some dependencies if you don't want to use certain commands.
3. Get a bot token for Telegram, through @BotFather.
4. Get your user ID for Telegram, through @myidbot.
5. Modify `default.conf` and configure whatever you would like.
6. Configure each plugin's configuration as specified in their files.
7. Run the bot in one of two ways:
   ```
   ./kadebot.py --config file.conf
   python3 kadebot.py --config file.conf
   ```

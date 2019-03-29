# kadebot-next

A next-gen Telegram chat bot, built in Python. The whole idea of this "next" version of kadebot is to move towards removing direct commands and instead parsing natural conversations to provide useful help. There will be multiple ways to do this by way of what I'm going to call "intent providers". Initially development is going to be done with [wit.ai](https://wit.ai) as the sole intent provider, but I do intend to make it easy to support others like DialogFlow.

# Roadmap

- [x] Implement configuration reader
- [ ] Re-make main process loop
- [ ] Implement an intent provider
  - [ ] wit.ai
  - [ ] DialogFlow
- [ ] Re-make many kadebot commands to fit the new paradigm
  - [ ] Weather
  - [ ] Movie info
  - [ ] Wikipedia Search
  - [ ] Others to be added

## Configuration

The base set of configuration requires you to specify your Telegram bot token, any administrators (people you want to have access to /reload, /update, /kill), and you may disable any command, monitor, scheduled task, or even entire module you don't want to use. For example, your base section may look like this:
```ini
[kadebot]
api_key = thisisa:keyfromtelegram
admins = 1234567890,8888888888
```

## Development

1. Clone the repository.
2. Install the required dependencies for whichever modules you are using. If you want to use everything:
   ```
   pip install -r requirements.txt
   ```
   You may need to run as `sudo` or with the `--user` flag if you don't have `sudo` priveledges.
3. Get a bot token for Telegram, through @BotFather.
4. Get your user ID for Telegram, through @myidbot.
5. Modify `default.yaml` and configure whatever you would like. Optionally, copy the configuration to `~/.config/kadebot/kadebot.yaml` to avoid using the `--config` option.
6. Configure each plugin's configuration as specified in their files.
7. Install in editable mode:
   ```
   pip install -e .
   ``` 
8. Run the bot in one of a few ways:
   ```
   kadebot
   kadebot --config file.yaml
   ```

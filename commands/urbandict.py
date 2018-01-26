# UrbanDictionary plugin
# Commands:
#   - /udrandom

import shlex
import requests
from .basic import CommandBase, CommandInfo

class UrbanDictionary(CommandBase):
    name = "UrbanDictionary"
    safename = "urbandictionary"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = []
    def get_help_msg(self, cmd):
        if cmd == "udrandom":
            return "Call /udrandom with no arguments to see a random UrbanDictionary definition."
    def execute(self, bot, update):
        try:
            data = requests.get('http://api.urbandictionary.com/v0/random').json()
            choice = data['list'][0]
            fmt = '<b>Word:</b> {}\n\n{}'
            defn = choice['description']
            if len(defn) > 100:
                defn = defn[:97] + '...'
            bot.send_message(chat_id = update.message.chat_id,
                             text = fmt.format(choice['word'], defn),
                             parse_mode = 'HTML',
                             disable_notification = 'True')
            self.logger.info("Command /udrandom executed successfully.")
        except Exception as e:
            self.logger.error(e)
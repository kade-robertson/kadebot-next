# UrbanDictionary plugin
# Commands:
#   - /udrandom
# Monitors: None
# Schedules: None
# Configuration: None

import shlex
import requests
from .basic import *

class UrbanDictionary(CommandBase):
    name = "UrbanDictionary"
    safename = "urbandictionary"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("udrandom", self.execute, "See a random UrbanDictionary definition.")
        ]
    def get_help_msg(self, cmd):
        if cmd == "udrandom":
            return "Call /udrandom with no arguments to see a random UrbanDictionary definition."
    @log_error
    def execute(self, bot, update, args):
        data = requests.get('http://api.urbandictionary.com/v0/random').json()
        choice = data['list'][0]
        fmt = '<b>Word:</b> <a href="{}">{}</a>\n<b>Definition:</b> {}\n<b>Example:</b> <i>{}</i>'
        defn = choice['definition']
        if len(defn) > 300:
            defn = defn[:297] + '...'
        example = choice['example']
        if '\n' in example:
            example = '\n'+example
        bot.send_message(chat_id = update.message.chat_id,
                         text = fmt.format(
                             choice['permalink'], 
                             choice['word'], 
                             defn, 
                             example
                         ),
                         parse_mode = 'HTML',
                         disable_notification = True,
                         disable_web_page_preview = True)
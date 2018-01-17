# Dog plugin
# Commands:
#   - /dog
# Configuration: None

import shlex
import requests
from .basic import *

class Dog(CommandBase):
    name = "Dog"
    safename = "dog"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("dog", self.execute, "Displays a random dog image.")
        ]
    def get_help_msg(self, cmd):
        return ("Call /dog with no arguments for a general random image.\n"
                "Call /dog <breed> to get a random image for a specific breed.")
    def dogify(self, lst):
        out = ""
        for item in lst[::-1]:
            if item == 'ibizan':
                out += 'Ibizan/'
            else:
                out += item + '/'
        return out[:-1]
    def execute(self, bot, update):
        try:
            args = shlex.split(update.message.text)
            if len(args) == 1:
                data = requests.get("https://dog.ceo/api/breeds/image/random").json()
            elif len(args) == 2:
                name = self.dogify(args[1].lower().split(' ')[::-1])
                urlfmt = "https://dog.ceo/api/breed/{0}/images/random"
                data = requests.get(urlfmt.format(name)).json()
            else:
                name = self.dogify([x.lower() for x in args[1:]])
                urlfmt = "https://dog.ceo/api/breed/{0}/images/random"
                data = requests.get(urlfmt.format(name)).json()
            bot.send_photo(chat_id = update.message.chat_id, 
                           photo = data["message"],
                           disable_notification = True)
            self.logger.info("/dog executed successfully.")
        except Exception as e:
            self.logger.exception(e)

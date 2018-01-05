# Dog plugin
# Commands:
#   - /dog
# Configuration: None

import requests
from .basic import CommandBase

class Dog(CommandBase):
    name = "Dog"
    safename = "dog"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [("dog", self.execute, "Displays a random dog image.")]
    def get_help_msg(self, cmd):
        return "Call /dog with no arguments."
    def execute(self, bot, update):
        try:
            data = requests.get("https://dog.ceo/api/breeds/image/random").json()
            bot.send_photo(chat_id = update.message.chat_id, 
                           photo = data["message"],
                           disable_notification = True)
            self.logger.info("/dog executed successfully.")
        except Exception as e:
            self.logger.exception(e)

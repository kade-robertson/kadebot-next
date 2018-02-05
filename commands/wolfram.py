# WolframAlpha plugin
# Commands:
#   - /wolfram
# Configuration:
# command.wolfram:
#   api_key: "wolfram alpha api key"

import shlex
import wolframalpha
from .basic import *

class Wolfram(CommandBase):
    name = "Wolfram"
    safename = "wolfram"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("wolfram", self.execute, "Ask Wolfram Alpha a question.")
        ]
    def load_config(self, confdict):
        self.api = wolframalpha.Client(confdict["api_key"])
    def get_help_msg(self, cmd):
        return "Usage: /wolfram <question>"
    @bot_command
    def execute(self, bot, update, args):
        res = self.api.query(" ".join(args))
        bot.send_message(chat_id = update.message.chat_id, 
                         text = next(res.results).text,
                         disable_notification = True)

import shlex
import wolframalpha
from .basic import CommandBase

class Wolfram(CommandBase):
    name = "Wolfram"
    safename = "wolfram"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [("wolfram", self.execute, "Ask Wolfram Alpha a question.")]
    def load_config(self, confdict):
        self.api = wolframalpha.Client(confdict["api_key"])
    def get_help_msg(self, cmd):
        return "Usage: /wolfram <question>"
    def execute(self, bot, update):
        try:
            res = self.api.query(" ".join(shlex.split(update.message.text)[1:]))
            bot.send_message(chat_id = update.message.chat_id, 
                             text = next(res.results).text,
                             disable_notification = True)
            self.logger.info("/wolfram executed successfully.")
        except Exception as e:
            self.logger.exception(e)

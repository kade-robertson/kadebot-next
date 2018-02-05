# Eightball plugin
# Commands:
#   - /8ball
# Configuration: None

import random
from .basic import *

class EightBall(CommandBase):
    name = "8-ball"
    safename = "eightball"
    options = ["It is certain",
               "It is decidedly so",
               "Without a doubt",
               "Yes definitely",
               "You may rely on it",
               "As I see it, yes",
               "Most likely",
               "Outlook good",
               "Yes",
               "Signs point to yes",
               "Reply hazy try again",
               "Ask again later",
               "Better not tell you now",
               "Cannot predict now",
               "Concentrate and ask again",
               "Don't count on it",
               "My reply is no",
               "My sources say no",
               "Outlook not so good",
               "Very doubtful"]
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("8ball", self.execute, "Shake an 8-ball.")
        ]
    def get_help_msg(self, cmd):
        return "Call /8ball with no arguments."
    @log_error
    def execute(self, bot, update, **kwargs):
        bot.send_message(chat_id = update.message.chat_id, 
                         text = "The 8-ball says: {}".format(random.choice(self.options)),
                         disable_notification = True)

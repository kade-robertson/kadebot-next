# Example plugin
# Commands: None
# Monitors: None
# Schedules: None
# Configuration None

from .basic import *

class ExamplePugin(CommandBase):
    name = "Example"
    safename = "example"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("example", self.execute, "An example plugin.")
        ]
    def get_help_msg(self, cmd):
        return "{} is an example command which does nothing.".format(cmd)
    @log_error
    def execute(self, bot, update, args):
        if len(args) == 1:
            bot.send_message(chat_id = update.message.chat_id, 
                             text = "Hello, world!",
                             disable_notification = True)
        else:
            bot.send_message(chat_id = update.message.chat_id, 
                             text = "Hello, {}!".format(args[0]),
                             disable_notification = True)

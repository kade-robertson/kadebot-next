# Randomaww plugin
# Commands:
#   - /randomaww
# Configuration:
# command.randomaww:
#   client_id: "reddit client_id"
#   client_secret: "reddit client_secret"
#   user_agent: "name of your bot"

import praw
from .basic import *

class RandomAww(CommandBase):
    name = "RandomAww"
    safename = "randomaww"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("randomaww", self.execute, "Displays a random image from /r/aww.")
        ]
    def load_config(self, confdict):
        self.api = praw.Reddit(client_id = confdict["client_id"],
                               client_secret = confdict["client_secret"],
                               user_agent = confdict["user_agent"])
        self.api.read_only = True
    def get_help_msg(self, cmd):
        return "Call /randomaww with no arguments."
    @log_error
    def execute(self, bot, update, args):
        aww = self.api.subreddit('aww')
        post = aww.random()
        while post.post_hint != "image":
            post = aww.random()
        bot.send_photo(chat_id = update.message.chat_id, 
                       photo = post.url,
                       disable_notification = True)

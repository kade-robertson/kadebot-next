import praw
from .basic import CommandBase

class RandomAww(CommandBase):
    name = "RandomAww"
    safename = "randomaww"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [("randomaww", self.execute, "Displays a random image from /r/aww.")]
    def load_config(self, confdict):
        self.api = praw.Reddit(client_id = confdict["client_id"],
                               client_secret = confdict["client_secret"],
                               user_agent = condfdict["user_agent"])
        self.api.read_only = True
    def get_help_msg(self, cmd):
        return "Call /randomaww with no arguments."
    def execute(self, bot, update):
        try:
            aww = self.api.subreddit('aww')
            post = aww.random()
            while post.post_hint != "image":
                post = aww.random()
            bot.send_photo(chat_id = update.message.chat_id, 
                           photo = post.url,
                           disable_notification = True)
            self.logger.info("Command /randomaww executed successfully.")
        except Exception as e:
            self.logger.exception(e)

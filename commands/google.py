# Google plugin
# Commands:
#   - /google, /g
# Monitors: None
# Schedules: None
# Configuration: None

import urllib.parse
from .basic import *

class Google(CommandBase):
    name = "Google"
    safename = "google"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("google", self.execute, "Send a Google search link.", alias='g')
        ]
    def get_help_msg(self, cmd):
        return "/{} <search> will produce a direct link to the Google search results for that query.".format(cmd)
    @bot_command
    def execute(self, bot, update, args):
        search = ' '.join(update.message.text.split(' ')[1:])
        gurl = 'https://www.google.ca/search?q={}'.format(urllib.parse.quote_plus(search))
        output = '<a href="{}">view results</a>'.format(gurl)
        bot.send_message(chat_id = update.message.chat_id,
                         text = output,
                         parse_mode = 'HTML',
                         disable_notification = True,
                         disable_web_page_preview = True)

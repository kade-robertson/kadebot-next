# XKCD Plugin
# Commands:
#   - /xkcd
#   - /xkcdr
# Monitors: None
# Schedules: None
# Configuration: None

import shlex
import requests
from .basic import *

class XKCD(CommandBase):
    name = "XKCD"
    safename = "xkcd"
    def __init__(self, logger):
        super().__init__(logger)
        self.sess = requests.Session()
        self.to_register = [
            CommandInfo("xkcd", self.execute, "View an XKCD comic."),
            CommandInfo("xkcdr", self.execute_random, "View a random XKCD comic.")
        ]
    def on_exit(self):
        self.sess.close()
    def get_help_msg(self, cmd):
        if cmd == 'xkcd':
            return 'Call /xkcd <id> to obtain a particular comic.'
        else:
            return 'Call /xkcdr with no arguments to view a random comic.'
    def send_comic(self, bot, update, comicid):
        comicurl = 'https://xkcd.com/{}/'.format(comicid)
        comic = self.sess.get(comicurl).json()
        msg = '<b>Link:</b> {}\n'.format(comicurl, comic['title'])
        msg += '<b>Date:</b> {}-{}-{}\n'.format(
            comic['year'].zfill(4), comic['month'].zfill(2), comic['day'].zfill(3)
        )
        msg += '<b>Alt Text</b>: {}'.format(comic['alt'])
        bot.send_photo(chat_id = update.message.chat_id,
                       photo = comic['img'],
                       caption = '#{}: {}'.format(comic['num'], comic['title']),
                       disable_notification = True)
        bot.send_message(chat_id = update.message.chat_id,
                         text = msg,
                         parse_mode = 'HTML',
                         disable_notification = True,
                         disable_web_page_preview = True)
    def execute(self, bot, update):
        try:
            args = shlex.split(update.message.text)
            if len(args) != 2:
                return
            self.send_comic(bot, update, args[1])
            self.logger.info("Command /xkcd executed successfully")
        except Exception as e:
            self.logger.error(e)
    def execute_random(self, bot, update):
        try:
            self.logger.info("Command /xkcdr executed successfully")
        except Exception as e:
            self.logger.error(e)
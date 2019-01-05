# XKCD Plugin
# Commands:
#   - /xkcd
#   - /xkcdr
# Monitors: None
# Schedules: None
# Configuration: None

import shlex
import requests
from .basic import CommandBase, CommandInfo, bot_command

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
        if comicid == '404':
            bot.send_message(chat_id = update.message.chat_id,
                             text = '404: Comic Not Found',
                             disable_notification = True)
            return
        comicurl = 'https://xkcd.com/{}/'.format(comicid)
        comic = self.sess.get(comicurl + 'info.0.json')
        if comic.status_code != 200:
            bot.send_message(chat_id = update.message.chat_id,
                             text = '404: Comic Not Found',
                             disable_notification = True)
            return
        comic = comic.json()
        msg = '<b>Link:</b> <a href="{}">{}</a>\n'.format(comicurl, comic['title'])
        msg += '<b>Date:</b> {}-{}-{}\n'.format(
            comic['year'].zfill(4), comic['month'].zfill(2), comic['day'].zfill(2)
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
    @bot_command
    def execute(self, bot, update, args):
        if len(args) != 1:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This doesn't seem like correct usage of /xkcd.",
                             disable_notification = True)
            return
        self.send_comic(bot, update, args[0])
    @bot_command
    def execute_random(self, bot, update, args):
        newl = self.sess.get('https://c.xkcd.com/random/comic/').url
        self.send_comic(bot, update, newl.split('.com/')[1].split('/')[0])
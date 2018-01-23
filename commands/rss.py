# Popular times plugin
# Commands:
#   - /popular
# Monitors: None
# Configuration:
# command.rss:
#   data_dir: "path/to/storage"

import os
import glob
import requests
import datetime
import feedparser
from telegram import ParseMode
from .basic import *

class RSS(CommandBase):
    name = "RSS"
    safename = "rss"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("rss", self.execute_rss, "Schedule RSS updates."),
            CommandInfo("check_rss", self.setup_rss, )
        ]
        self.feeddict = dict()
    def get_help_msg(self, cmd):
        return "Register an RSS feed with /rss <url> <interval>. Valid intervals are 5m, 15m, 1h, 3h."
    def load_config(self, confdict):
        self.datadir = confdict['data_dir']
        self.feeddict = dict()
        if not os.path.exists(self.datadir):
            os.mkdir(self.datadir)
        else:
            for fn in glob.glob(os.path.join(self.datadir, '*.groupfeeds')):
                shortfn = os.path.splitext(os.path.basename(fn))[0]
                with open(fn, 'r') as f:
                    toreg = [x.strip().split('\t') for x in f.readlines()]
                    self.feeddict[shortfn] = []
                    for feedurl, interval, lastid in toreg:
                        self.feeddict[shortfn].append((feedurl, int(interval), lastid))
    def on_exit(self):
        if not os.path.exists(self.datadir):
            os.mkdir(self.datadir)
        for chat_id in self.feeddict.keys():
            with open(os.path.join(self.datadir, chat_id + '.groupfeeds'), 'w') as f:
                f.write('\n'.join('\t'.join(map(str, x)) for x in self.feeddict['keys']))
    def setup_rss(self, updater):
        stagger = 0
        self.temp_upd = updater
        for chatid in self.feeddict.keys():
            for url, intsec, last in self.feeddict[chatid]:
                updater.job_queue.run_repeating(
                    self.check_rss, 
                    interval=datetime.timedelta(seconds=intsec),
                    context=(chatid, (url, intsec, last)),
                    first = stagger
                )
                stagger += 5
    def check_rss(self, bot, job):
        chat_id, meta = job.context
        feedurl, interval, last_id = meta
        try:
            feed = feedparser.parse(feedurl)
            if len(feed['entries']) > 0:
                recent = feed['entries'][0]
                if recent['id'] != last_id:
                    out = 'Feed Update: <a href="{}">{}</a>'.format(recent['link'], recent['description'])
                    bot.send_photo(chat_id = chat_id 
                                   parse_mode = ParseMode.HTML,
                                   text = out,
                                   disable_notification = False)
                    self.feeddict[chat_id] = (feedurl, interval, recent['id'])
        except:
            pass
    def execute_rss(self, bot, update):
        try:
            args = shlex.split(update.message.text)
            if len(args) != 3:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem like correct usage of /rss.",
                                 disable_notification = True)
                return
            attempt = requests.head(args[1])
            if attempt.status_code != 200:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem to be a valid link.",
                                 disable_notification = True)
                return
            if args[2] not in ('5m', '15m', '1h', '3h'):
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem to be a valid interval.",
                                 disable_notification = True)
                return
            interval = 300
            if args[2] == '15m':
                interval *= 3
            elif args[2] == '1h':
                interval *= 12
            elif args[2] == '3h':
                interval *= 36
            curid = feedparser.parse(args[1])['entries'][0]['id']
            if not args[1] in [x[0] for x in self.feeddict[update.message.chat_id]]:
                self.feeddict[update.message.chat_id].append((args[1], interval, curid))
                self.temp_upd.job_queue.run_repeating(
                    self.check_rss,
                    interval=datetime.timedelta(seconds=interval),
                    context=(update.message.chat_id, (args[1], interval, curid))
                )
            self.logger.info("Command /rss executed successfully.")
        except Exception as e:
            self.logger.error(e)
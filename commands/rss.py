# Popular times plugin
# Commands:
#   - /popular
# Monitors: None
# Configuration:
# command.rss:
#   data_dir: "path/to/storage"

import os
import glob
import datetime
import feedparser
from telegram import ParseMode
from .basic import *

class RSS(CommandBase):
    name = "RSS"
    safename = "rss"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = []
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
    def setup_rss(self, updater):
        for chatid in self.feeddict.keys():
            for url, intsec, last in self.feeddict[chatid]:
                updater.job_queue.run_repeating(
                    check_rss, 
                    interval=datetime.timedelta(seconds=intsec),
                    context=(chatid, (url, intsec, last))
                )
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
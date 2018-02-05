# Random Date Fact plugin
# Commands:
#   - /today
#   - /todayreg
# Monitors: None
# Schedules: fact_today
# Configuration:
# command.dayfact:
#   datfile: "path/to/datfile.txt"

import os
import shlex
import datetime
import requests
from .basic import *

class TodayFact(CommandBase):
    name = "TodayFact"
    safename = "todayfact"
    def __init__(self, logger):
        super().__init__(logger)
        self.sched_chats = dict()
        self.to_register = [
            CommandInfo("today", self.execute, "See facts about today."),
            CommandInfo("todayreg", self.execute_sched, "Schedule daily facts for this chat."),
            CommandInfo("todaydel", self.execute_del, "Remove scheduled daily facts for this chat."),
            CommandInfo("fact_today", self.setup_facts, "Show scheduled daily facts", _type=CommandType.Schedule)
        ]
    def get_help_msg():
        return ""
    def load_config(self, confdict):
        self.regfile = confdict['datfile']
        if os.path.isfile(self.regfile):
            with open(self.regfile, 'r') as f:
                lines = [x.strip().split(' ') for x in f.readlines()]
                for chat, hour in lines:
                    self.sched_chats[int(chat)] = int(hour)
    def on_exit(self):
        if os.path.isfile(self.regfile):
            os.remove(self.regfile)
        if self.sched_chats:
            with open(self.regfile, 'w') as f:
                f.write('\n'.join(' '.join(map(str, x)) for x in self.sched_chats.items()))
    def send_stats(self, bot, chatid):
        today = datetime.datetime.today()
        ending = 'th'
        if today.day % 10 == 1:
            ending = 'st'
        elif today.day % 10 == 2:
            ending = 'nd'
        elif today.day % 10 == 3:
            ending = 'rd'
        todaystr = '{} {}{}'.format(today.strftime('%B'), today.day, ending)
        output = "*{}*:".format(todaystr)
        with requests.Session() as sess:
            data = set()
            tries = 15
            while len(data) != 5 and tries > 0:
                data.add(sess.get(
                    'http://numbersapi.com/{}/{}/date'.format(today.month, today.day)
                ).text.replace(todaystr, ''))
                tries -= 1
            data = sorted(data, key=lambda x: int(x.split()[4]))
            output += '\n' + '\n'.join(' -{}'.format(x) for x in data)
        bot.send_message(
            chat_id = chatid,
            text = output,
            parse_mode = 'MARKDOWN',
            disable_notification = True
        )
    @bot_command
    def execute(self, bot, update, args):
        self.send_stats(bot, update.message.chat_id)
    def setup_facts(self, updater):
        self.temp_upd = updater
        if self.sched_chats is not None:
            for key, hour in self.sched_chats.items():
                updater.job_queue.run_daily(
                    self.execute_today,
                    time = datetime.time(hour, 0, 0),
                    context = key
                )
    @bot_command
    def execute_sched(self, bot, update, args):
        if len(args) != 1:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This doesn't seem like correct usage of /rss.",
                             disable_notification = True)
            return
        if not args[0].isdigit() and 0 <= int(args[0]) <= 23:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This is not a valid hour (0 <= hour <= 23).",
                             disable_notification = True)
            return
        if update.message.chat_id in self.sched_chats.keys():
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This chat has daily facts scheduled already.",
                             disable_notification = True)
            return
        self.sched_chats[update.message.chat_id] = int(args[0])
        self.temp_upd.job_queue.run_daily(
            self.execute_today,
            time = datetime.time(int(args[0]), 0, 0),
            context = update.message.chat_id
        )
        bot.send_message(chat_id = update.message.chat_id,
                         text = "Daily facts have been scheduled.",
                         disable_notification = True)
    @bot_command
    def execute_del(self, bot, update, args):
        if update.message.chat_id in self.sched_chats.keys():
            del self.sched_chats[update.message.chat_id]
            bot.send_message(chat_id = update.message.chat_id,
                             text = "Daily facts have been disabled.",
                             disable_notification = True)
    def execute_today(self, bot, job):
        try:
            if self.sched_chats is None or not job.context in self.sched_chats.keys():
                job.schedule_removal()
                return
            self.send_stats(bot, job.context)
            self.logger.info("day_fact schedule completed successfully.")
        except Exception as e:
            self.logger.error(e)
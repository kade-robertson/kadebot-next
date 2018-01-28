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
from .basic import CommandBase, CommandInfo, CommandType

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
            for i in range(5):
                data = sess.get(
                    'http://numbersapi.com/{}/{}/date'.format(today.month, today.day)
                ).text
                output += "\n -{}".format(data.replace(todaystr, ''))
        bot.send_message(
            chat_id = chatid,
            text = output,
            parse_mode = 'MARKDOWN',
            disable_notification = True
        )
    def execute(self, bot, update):
        try:
            self.send_stats(bot, update.message.chat_id)
            self.logger.info("Command /today executed successfully.")
        except Exception as e:
            self.logger.error(e)
    def setup_facts(self, updater):
        self.temp_upd = updater
        if self.sched_chats is not None:
            for key, hour in self.sched_chats.items():
                updater.job_queue.run_daily(
                    self.execute_today,
                    time = datetime.time(hour, 0, 0),
                    context = key
                )
    def execute_sched(self, bot, update):
        try:
            args = shlex.split(update.message.text)
            if len(args) != 2:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem like correct usage of /todayreg.",
                                 disable_notification = True)
                return
            if not args[1].isdigit() and 0 <= int(args[1]) <= 23:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This is not a valid hour (0 <= hour <= 23).",
                                 disable_notification = True)
                return
            if update.message.chat_id in self.sched_chats.keys():
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This chat has daily facts scheduled already.",
                                 disable_notification = True)
                return
            self.sched_chats[update.message.chat_id] = int(args[1])
            self.temp_upd.job_queue.run_daily(
                self.execute_today,
                time = datetime.time(int(args[1]), 0, 0),
                context = update.message.chat_id
            )
            bot.send_message(chat_id = update.message.chat_id,
                             text = "Daily facts have been scheduled.",
                             disable_notification = True)
            self.logger.info("Command /todayreg executed successfully.")
        except Exception as e:
            self.logger.error(e)
    def execute_del(self, bot, update):
        try:
            if update.message.chat_id in self.sched_chats.keys():
                del self.sched_chats[update.message.chat_id]
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "Daily facts have been disabled.",
                                 disable_notification = True)
            self.logger.info("Command /todaydel executed successfully.")
        except Exception as e:
            self.logger.error(e)
    def execute_today(self, bot, job):
        try:
            if self.sched_chats is None or not job.context in self.sched_chats.keys():
                job.schedule_removal()
                return
            self.send_stats(bot, job.context)
            self.logger.info("day_fact schedule completed successfully.")
        except Exception as e:
            self.logger.error(e)
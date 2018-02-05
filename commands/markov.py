# Markov plugin
# Commands:
#   - /markov
# Monitors:
#   - markov_monitor
# Configuration:
# command.markov:
#   folder: "markov data folder"

import os
import json
import markovify
from .basic import *

class Markov(CommandBase):
    name = "Markov"
    safename = "markov"
    datfolder = ""
    users = dict()
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("markov", self.execute_generate, "Emulate yourself talking."),
            CommandInfo("markov_monitor", self.monitor_modeling, "Model users.", _type=CommandType.Monitor)
        ]
    def get_help_msg(self, cmd):
        return "Call /markov to have the Markov model generate text that sounds like you."
    def load_config(self, confdict):
        self.datfolder = confdict['folder']
        if os.path.exists(self.datfolder):
            for file in os.listdir(self.datfolder):
                with open(os.path.join(self.datfolder, file), 'r', newline='\n') as f:
                    udata = f.read()
                    user = file.split('.json')[0]
                    ujson = json.loads(udata)
                    data = markovify.Text.from_dict(ujson)
                    self.users[user] = data
    def on_exit(self):
        self.logger.info("  Saving collected Markov data..")
        if not os.path.exists(self.datfolder):
            os.makedirs(self.datfolder)
        for user in self.users:
            udata = self.users[user].to_json()
            with open(os.path.join(self.datfolder, '{}.json'.format(user)), 'w', newline='\n') as f:
                f.write(udata)
        self.logger.info("  Done saving.")
    @log_error
    def execute_generate(self, bot, update, **kwargs):
        user = 'markov_model'
        if user in self.users:
            out = None
            while out == None:
                out = self.users[user].make_sentence()
            bot.send_message(chat_id = update.message.chat_id,
                             text = out,
                             disable_notification = True)
        else:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "I currently have no data from you, try later.",
                             disable_notification = True)
    def monitor_modeling(self, bot, update):
        try:
            user = 'markov_model'
            intext = update.message.text
            if intext[-1] not in '.!?':
                intext += '.'
            new = markovify.Text(intext, state_size = 3)
            self.logger.info("  Adding to a Markov model..")
            if user not in self.users:
                self.users[user] = new
            else:
                self.users[user] = markovify.combine(models=[self.users[user], new])
            self.logger.info("  Adding done.")
            self.logger.info("markov_monitor processing completed successfully.")
        except Exception as e:
            self.logger.error(e)

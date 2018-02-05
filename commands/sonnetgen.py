# SonnetGen plugin
# Commands:
#   - /sonnetgen
# Monitors: None
# Configuration: None

import os
import markovify
from .basic import *

dat = None

class SonnetGen(CommandBase):
    name = "SonnetGen"
    safename = "sonnetgen"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("sonnetgen", self.execute, "Generate a brand-new Shakespeare sonnet."),
        ]
    def get_help_msg(self, cmd):
        return "Call /sonnetgen with no arguments."
    @log_error
    def execute(self, bot, update, args):
        with open('shakespeare/sonnets.json', 'r') as f:
            dat = markovify.NewlineText.from_json(f.read())
        out = [dat.make_sentence()]
        while out[-1][-1] not in '.!?' or len(out) < 5:
            out.append(dat.make_sentence())
        bot.send_message(chat_id = update.message.chat_id,
                         text = '\n'.join(out),
                         disable_notification = True)
        self.logger.info("Command /sonnetgen completed successfully.")
            
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
        self.to_register = [
            CommandInfo("xkcd", self.execute, "View an XKCD comic."),
            CommandInfo("xkcdr", self.execute_random, "View a random XKCD comic.")
        ]
    def get_help_msg(self, cmd):
        if cmd == 'xkcd':
            return 'Call /xkcd <id> to obtain a particular comic.'
        else:
            return 'Call /xkcdr with no arguments to view a random comic.'
    def execute(self, bot, update):
        try:
            self.logger.info("Command /xkcd executed successfully")
        except Exception as e:
            self.logger.error(e)
    def execute_random(self, bot, update):
        try:
            self.logger.info("Command /xkcdr executed successfully")
        except Exception as e:
            self.logger.error(e)
# Popular times plugin
# Commands:
#   - /popular
# Monitors: None
# Configuration:
# command.populartimes:
#   api_key: "Google Places API Key"

import shlex
from .basic import *

class PopularTimes(CommandBase):
    name = "PopularTimes"
    safename = "populartimes"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("popular", self.execute, "See busy times for a place.")
        ]
    def load_config(self, confdict):
        self.apikey = confdict["api_key"]
    def get_help(self, cmd):
        return "Call /popular <lat>,<lng> to see the busy times for that place."
    def execute(self, bot, update):
        pass
    
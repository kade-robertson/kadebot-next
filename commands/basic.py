from enum import Enum
from telegram.ext import Filters

class CommandType(Enum):
    Default = 0
    Monitor = 1

class CommandInfo:
    def __init__(self, name, func, shorthelp, _type=CommandType.Default, alias=None, filter=Filters.text):
        self.name = name
        self.func = func
        self.helpmsg = shorthelp
        self.type = _type
        self.alias = alias
        self.filter = filter

class CommandBase:
    name = "BaseCommand"
    safename = "basecommand"
    description = "Not an actual command, inherit this!"
    def __init__(self, logger):
        self.logger = logger
        self.to_register = []
    def on_exit(self):
        pass
    def load_config(self, confdict):
        pass
    def get_help_msg(self, cmd):
        raise NotImplementedError
    def execute(self, bot, update):
        raise NotImplementedError
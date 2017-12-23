import shlex

class CommandBase:
    name = "BaseCommand"
    safename = "basecommand"
    description = "Not an actual command, inherit this!"
    def __init__(self, logger):
        self.logger = logger
        self.to_register = []
    def load_config(self, confdict):
        raise NotImplementedError
    def get_help_msg(self):
        raise NotImplementedError
    def execute(self, bot, update):
        raise NotImplementedError
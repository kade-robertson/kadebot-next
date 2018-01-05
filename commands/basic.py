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
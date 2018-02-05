# Translate plugin
# Commands:
#   - /t
# Configuration:
# command.translate:
#   api_key: "microsoft translate api key" (optional)

import shlex
from translate import Translator
from .basic import *

class Translate(CommandBase):
    name = "Translate"
    safename = "translate"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("translate", self.execute, "Translate text to English.", alias="t")
        ]
    def load_config(self, confdict):
        if confdict is not None and "api_key" in confdict.keys():
            self.translator = Translator(provider = "microsoft", 
                                         from_lang = "autodetect",
                                         to_lang = "en",
                                         secret_access_key = confdict["api_key"])
        else:
            self.translator = Translator(from_lang = "autodetect", to_lang = "en")
    def get_help_msg(self, cmd):
        return "Call /{} <string> to translate any string to English.".format(cmd)
    @log_error
    def execute(self, bot, update, args):
        text = " ".join(args)
        new = self.translator.translate(text)
        bot.send_message(chat_id = update.message.chat_id,
                         text = "Translation: {}".format(new),
                         disable_notification = True)

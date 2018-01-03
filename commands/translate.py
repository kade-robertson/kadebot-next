from langdetect import detect, DetectorFactory
from translate import Translator
DetectorFactory.seed = 0
import shlex
from .basic import CommandBase

class Translate(CommandBase):
    name = "Translate"
    safename = "translate"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [("t", self.execute, "Translate text to English.")]
    def load_config(self, confdict):
        if confdict is not None and "api_key" in confdict.keys():
            self.translator = Translator(provider = "microsoft", 
                                         from_lang = "autodetect",
                                         to_lang = "en",
                                         secret_access_key = confdict["api_key"])
        else:
            self.translator = Translator(from_lang = "autodetect", to_lang = "en")
    def get_help_msg(self, cmd):
        return "Call /t <string> to translate any string to English."
    def execute(self, bot, update):
        try:
            text = " ".join(shlex.split(update.message.text)[1:])
            new = self.translator.translate(text)
            bot.send_message(chat_id = update.message.chat_id,
                             text = "Translation: {}".format(new),
                             disable_notification = True)
            self.logger.info("Command /t executed successfully.")
        except Exception as e:
            self.logger.exception(e)

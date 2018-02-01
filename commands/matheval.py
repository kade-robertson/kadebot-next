# Math evaluation plugin
# Commands:
#   - /math
# Monitors: None
# Schedules: None
# Configuration: None

import shlex
from py_expression_eval import Parser
from .basic import *

class MathEval(CommandBase):
    name = "MathEval"
    safename = "math"
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("math", self.execute, "Evaluate a simple math expression")
        ]
    def get_help_msg(self, cmd):
        return "Call /math <expr> to compute the result of an expression."
    def execute(self, bot, update):
        try:
            expr = shlex.split(update.message.text)
            if len(expr) > 2:
                expr = ' '.join(expr[1:])
            elif len(expr) == 2:
                expr = expr[1]
            else:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem like correct usage of /math.",
                                 disable_notification = True)
                return
            p = Parser()
            bot.send_message(chat_id = update.message.chat_id,
                             text = "Result: {}".format(p.parse(expr).evaluate({})),
                             disable_notification = True)
            self.logger.info('Command /math executed successfully.')
        except Exception as e:
            bot.send_photo(chat_id = update.message.chat_id,
                           photo = r'http://i3.kym-cdn.com/photos/images/newsfeed/000/234/739/fa5.jpg',
                           disable_notification = True)
            self.logger.error(e)
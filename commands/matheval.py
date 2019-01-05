# Math evaluation plugin
# Commands:
#   - /math
# Monitors: None
# Schedules: None
# Configuration: None

import shlex
from py_expression_eval import Parser
from .basic import CommandBase, CommandInfo, bot_command

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
    @bot_command
    def execute(self, bot, update, **kwargs):
        expr = kwargs.get('args')
        if len(expr) > 1:
            expr = ' '.join(expr)
        elif len(expr) == 1:
            expr = expr[0]
        else:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This doesn't seem like correct usage of /math.",
                             disable_notification = True)
            return
        p = Parser()
        bot.send_message(chat_id = update.message.chat_id,
                         text = "Result: {}".format(p.parse(expr).evaluate({})),
                         disable_notification = True)

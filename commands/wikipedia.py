# Wikipedia plugin
# Commands:
#   - /wiki
#   - /wikisearch
# Configuration: None

import shlex
import wikipedia
from .basic import *

class Wikipedia(CommandBase):
    name = 'Wikipedia'
    safename = 'wikipedia'
    def __init__(self, logger):
        super().__init__(logger)
        self.to_register = [
            CommandInfo("wiki", self.execute_summary, "Displays a Wikipedia summary."),
            CommandInfo("wikisearch", self.execute_search, "Searches for a Wikipedia article.")
        ]
    def get_help_msg(self, cmd):
        if cmd == "wiki":
            return 'Call /wiki <page> with the Wikipedia article you want the summary for.'
        elif cmd == "wikisearch":
            return ('Call /wikisearch <search> with the article you wish to search for, '
                    'using quotes if there are spaces.')
    @log_error
    def execute_summary(self, bot, update, args):
        if len(args) != 1:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This doesn't seem like correct usage of /wiki.",
                             disable_notification = True)
            return
        output = wikipedia.summary(args[0], sentences = 4).replace(" ( listen) ", "")
        bot.send_message(chat_id = update.message.chat_id,
                         text = output,
                         disable_notification = True)
    @log_error
    def execute_search(self, bot, update):
        if len(args) != 1:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This doesn't seem like correct usage of /wikisearch.",
                                disable_notification = True)
            return
        results = wikipedia.search(args[0]])
        output = "Available articles:\n" + \
                 '\n'.join(" - {}".format(res) for res in results[:7])
        bot.send_message(chat_id = update.message.chat_id,
                         text = output,
                         disable_notification = True)

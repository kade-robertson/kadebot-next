# GRT plugin
# Commands:
#   - /grt
# Monitors: None
# Configuration: None

import shlex
import requests

class GRT(BaseCommand):
    name = "GRT"
    safename = "grt"
    def __init__(self, logger):
        super().__init__(logger)
    def get_help_msg(self, cmd):
        return "Call /grt <stop> <bus> to check bus times.
    def execute(self, bot, update):
        try:
            args = shlex.split(update.message.text)
            if len(args) != 3:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem like correct usage of /grt.",
                                 disable_notification = True)
                return
            params = { 'stopId': args[1], 'routeId': args[2] }
            data = requests.get(r"http://realtimemap.grt.ca/Stop/GetStopInfo", params=params).json()
            times = data['stopTimes']
            if len(times) == 0:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "There are no times available for this query.",
                                 disable_notification = True)
                return
            times = sorted(set(times), key=lamdba x: x['Minutes'])
            output = "Times for the {} at stop {}: ".format(args[2], args[1])
            output += ", ".join(x['Minutes'] + ' minutes' for x in times)
            bot.send_message(chat_id = update.message.chat_id,
                             text = output,
                             disable_notification = True)
            self.logger.info("Command /grt executes successfully.")
        except Exception as e:
            self.logger.error(e)
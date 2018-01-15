# Popular times plugin
# Commands:
#   - /popular
# Monitors: None
# Configuration:
# command.populartimes:
#   api_key: "Google Places API Key"

import json
import shlex
import requests
import populartimes
from itertools import groupby
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
    def get_help_msg(self, cmd):
        return "Call /popular \"<place>\" to see the busy times for that place."
    def execute(self, bot, update):
        try:
            args = shlex.split(update.message.text)
            if len(args) != 2:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem like correct usage of /popular.",
                                 disable_notification = True)
                return
            gparams = { "query": args[1], "key": self.apikey }
            req = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params = gparams)
            place_info = json.loads(req.text)["results"]
            if len(place_info) == 0:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "Unfortunately, I got no results for the place you searched.",
                                 disable_notification = True)
                return
            place_id = place_info[0]["place_id"]
            poptimes = populartimes.get_id(self.apikey, place_id)
            out = "Busy times for {}:\n".format(poptimes['name'])
            if len(poptimes['populartimes']) == 0:
                out += " - Unavailable!\n"
            for day in poptimes['populartimes']:
                out += " - {}: ".format(day['name'])
                # Order so the busy time list is from 6am to 5am
                data = [x >= 50 for x in day['data'][6:]+day['data'][:6]]
                busy = []
                for k, v in groupby(enumerate(data), key = lambda x: x[1]):
                    if k:
                        v = list(v)
                        start, end = divmod(v[0][0] + 6, 12), divmod(v[-1][0] + 6, 12)
                        tstr = "{}{}m".format(12 if end[1] == 0 else end[1], 'p' if end[0] == 1 else 'a')
                        if start != end:
                            tstr = "{}{}m-".format(12 if start[1] == 0 else start[1], 'p' if start[0] == 1 else 'a') + tstr
                        busy.append(tstr)
                out += "{}\n".format(', '.join(busy) if len(busy) > 0 else "None")
            if 'current_popularity' in poptimes.keys():
                cur = poptimes['current_popularity']
                is_busy = 'Not busy' if cur < 50 else 'Busy'
                out += "\nCurrent busyness: {} ({}%)".format(is_busy, cur)
            bot.send_message(chat_id = update.message.chat_id,
                             text = out,
                             disable_notification = True)
            self.logger.info("Command /popular executed successfully.")
        except Exception as e:
            self.logger.error(e)
    
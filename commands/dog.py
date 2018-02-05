# Dog plugin
# Commands:
#   - /dog
# Configuration: None

import shlex
import string
import requests
from .basic import *

_doggos = {
    'germanshepherd': 'German Shepherd',
    'stbernard': 'St. Bernard',
    'mexicanhairless': 'Mexican Hairless',
    'shihtzu': 'Shih Tzu',
    'westhighland terrier': 'West Highland Terrier'
}

class Dog(CommandBase):
    name = "Dog"
    safename = "dog"
    def __init__(self, logger):
        super().__init__(logger)
        self.breed_list = []
        self.to_register = [
            CommandInfo("dog", self.execute, "Displays a random dog image."),
            CommandInfo("dogsearch", self.execute_list, "Search for dog breeds."),
            CommandInfo("dogbreeds", self.breedsetup, "Get list of dog breeds.", 
                        _type=CommandType.Schedule)
        ]
    def get_help_msg(self, cmd):
        if cmd == "dog":
            return ("Call /dog with no arguments for a general random image.\n"
                    "Call /dog <breed> to get a random image for a specific breed.")
        elif cmd == "dogsearch":
            return "Call /dogsearch <breed> to search all breeds."
    def dogify(self, lst):
        out = ""
        for item in lst[::-1]:
            if item == 'ibizan':
                out += 'Ibizan/'
            else:
                out += item + '/'
        return out[:-1]
    @log_error
    def execute(self, bot, update, **kwargs):
        args = kwargs.get('args')
        if len(args) == 0:
            urlfmt = "https://dog.ceo/api/breeds/image/random"
        elif len(args) == 1:
            name = self.dogify(args[0].lower().split(' ')[::-1])
            urlfmt = "https://dog.ceo/api/breed/{0}/images/random".format(name)
        else:
            name = self.dogify([x.lower() for x in args])
            urlfmt = "https://dog.ceo/api/breed/{0}/images/random".format(name)
        self.logger.info(urlfmt)
        data = requests.get(urlfmt).json()
        self.logger.info(data['message'])
        if len(args) == 0:
            breed = data['message'].split('img/')[1].split('/')[0].replace('-', ' ')
            breed = ' '.join(breed.split(' ')[::-1])
            if breed in _doggos.keys():
                breed = _doggos[breed]
            else:
                breed = string.capwords(breed)
            bot.send_photo(chat_id = update.message.chat_id, 
                           photo = data["message"],
                           caption = breed,
                           disable_notification = True)
        else:
            bot.send_photo(chat_id = update.message.chat_id, 
                           photo = data["message"],
                           disable_notification = True)
    def breedsetup(self, updater):
        self.update_breeds()
        updater.job_queue.run_daily(self.update_breeds, None)
    def update_breeds(self):
        temp_list = []
        with requests.Session() as breed_sess:
            base_breeds = breed_sess.get('https://dog.ceo/api/breeds/list').json()
            for breed in base_breeds['message']:
                self.logger.info(" - Getting sub-breeds of {}...".format(breed))
                sub_breeds = breed_sess.get('https://dog.ceo/api/breed/{0}/list'.format(breed)).json()
                if len(sub_breeds['message']) == 0:
                    temp_list.append(breed)
                else:
                    for sub in sub_breeds['message']:
                        temp_list.append(' '.join([sub, breed]))
                self.logger.info(" - {} collection done.".format(breed))
        self.breed_list = temp_list
        self.logger.info("Scheduled task dogbreeds completed.")
    @log_error
    def execute_list(self, bot, update, **kwargs):
        if len(self.breed_list) == 0:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "Not available, breed list isn't populated.",
                             disable_notification = True)
            self.logger.info("/dogsearch had no list to search.")
            return
        args = kwargs.get('args')
        if len(args) != 1:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This doesn't seem like correct usage of /dogsearch.",
                             disable_notification = True)
            return
        out = "Search results: "
        res = sorted([x for x in self.breed_list if args[0].lower() in x.lower()])
        if len(res) == 0:
            out += "None!"
        else:
            for r in res[:7]:
                out += "\n - {}".format(r)
        bot.send_message(chat_id = update.message.chat_id, 
                         text = out,
                         disable_notification = True)

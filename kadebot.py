#!/usr/bin/python3

import os
import sys
import shlex
import argparse


from commands.cat import Cat
from commands.dog import Dog
from commands.eightball import EightBall
from commands.movie import Movie
from commands.translate import Translate
from commands.wikipedia import Wikipedia
from commands.wolfram import Wolfram

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from ruamel.yaml import YAML
yaml = YAML(typ="safe", pure=True)

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

baseconf = dict()
commands = [ Cat(logging),
             Dog(logging),
             EightBall(logging),
             Wolfram(logging),
             Movie(logging),
             Wikipedia(logging),
             Translate(logging) ]
regdhelp = dict()

def kill(bot, update):
    if update.message.from_user.id in baseconf["admins"]:
        logging.info("Admin killed the bot, shutting down.")
        sys.stdout.flush()
        os._exit(0)

def reload(bot, update):
    if update.message.from_user.id in baseconf["admins"]:
        logging.info("Reloading chat bot now...")
        python = sys.executable
        os.execv(python, ['python3'] + sys.argv)

def update(bot, update):
    if update.message.from_user.id in baseconf["admins"]:
        logging.info("Updating bot...")
        os.system("git pull --force")
        reload(bot, update)

def help(bot, update):
    args = shlex.split(update.message.text)
    if len(args) > 1:
        cmd = args[1]
        if cmd in regdhelp.keys():
            dat = regdhelp[cmd].get_help_msg(cmd)
            out = "Help for /{}:\n\n{}".format(cmd, dat)
            bot.send_message(chat_id = update.message.chat_id, 
                             text = out,
                             disable_notification = True)
    else:
        out = ""
        for cmd in commands:
            for name, func, msg in cmd.to_register:
                out += "/{} - {}\n".format(name, msg)
        bot.send_message(chat_id = update.message.chat_id, 
                         text = out,
                         disable_notification = True)

def error_handler(bot, update, error):
    try:
        raise error
    except Exception as e:
        logging.error(e)

def main():
    global regdhelp
    updater = Updater(token = baseconf["api_key"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("reload", reload))
    dispatcher.add_handler(CommandHandler("update", update))
    dispatcher.add_handler(CommandHandler("kill", kill))
    for cmd in commands:
        for name, func, msg in cmd.to_register:
            dispatcher.add_handler(CommandHandler(name, func))
            regdhelp[name] = cmd
            logging.info("Registered command /{}".format(name))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()

def load_config(filename):
    global baseconf
    global translator
    conf = dict()
    with open(filename, 'r') as f:
        conf = yaml.load(f)
    baseconf = conf["base"]
    for cmd in commands:
        section = "command.{}".format(cmd.safename)
        if section in conf.keys():
            cmd.load_config(conf[section])
        
if __name__ == "__main__":
    parser  = argparse.ArgumentParser()
    parser.add_argument("--config", help="configuration file to use", type=str)
    args = parser.parse_args()
    if os.path.exists(args.config):
        load_config(args.config)
        logging.info("Loaded configuration.")
        main()
    else:
        logging.error("No config file found.")
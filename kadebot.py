#!/usr/bin/python3

import os
import shlex
import argparse

from commands.cat import Cat
from commands.dog import Dog

from telegram.ext import Updater
from telegram.ext import CommandHandler
from ruamel.yaml import YAML
yaml = YAML(typ="safe", pure=True)

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

baseconf = dict()
commands = [Cat(logging),
            Dog(logging)]
regdhelp = dict()

def help(bot, update):
    args = shlex.split(update.message.text)
    if len(args) > 1:
        cmd = args[2]
        if cmd in regdhelp.keys():
            dat = regdhelp[cmd].get_help_msg(cmd)
            out = "Help for /{}\n\n{}".format(cmd, dat)
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

def main():
    global regdhelp
    updater = Updater(token = baseconf["api_key"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", help))
    for cmd in commands:
        for name, func, msg in cmd.to_register:
            dispatcher.add_handler(CommandHandler(name, func))
            regdhelp[name] = cmd
    updater.start_polling()

def load_config(filename):
    global baseconf
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
    main()
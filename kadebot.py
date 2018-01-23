#!/usr/bin/python3

import os
import sys
import shlex
import argparse
import importlib

import commands as _commands
from commands import CommandBase, CommandType, CommandInfo

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from ruamel.yaml import YAML
yaml = YAML(typ="safe", pure=True)

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

baseconf = dict()
commands = []
regdhelp = dict()

def kill(bot, update):
    if update.message.from_user.id in baseconf["admins"]:
        logging.info("Admin killed the bot, shutting down.")
        for cmd in commands:
            cmd.on_exit()
        logging.info("Cleanup done, exiting.")
        sys.stdout.flush()
        os._exit(0)

def reload(bot, update):
    if update.message.from_user.id in baseconf["admins"]:
        logging.info("Reloading chat bot now...")
        for cmd in commands:
            cmd.on_exit()
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
            for ci in cmd.to_register:
                if not ci.name in baseconf["disabled"] and ci.type == CommandType.Default:
                    if ci.alias != None:
                        out += "/{}, /{} - {}\n".format(ci.name, ci.alias, ci.helpmsg)
                    else:
                        out += "/{} - {}\n".format(ci.name, ci.helpmsg)
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
    global commands
    updater = Updater(token = baseconf["api_key"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("reload", reload))
    dispatcher.add_handler(CommandHandler("update", update))
    dispatcher.add_handler(CommandHandler("kill", kill))
    to_schedule = []
    for cmd in commands:
        for ci in cmd.to_register:
            if ci.name in baseconf["disabled"]:
                logging.info("Disabled command /{}".format(ci.name))
                continue
            if ci.name in baseconf["disabled_monitors"]:
                logging.info("Disabled monitor {}".format(ci.name))
                continue
            if ci.name in baseconf["disabled_schedules"]:
                logging.info("Disabled scheduled task {}".format(ci.name))
                continue
            if ci.type == CommandType.Default:
                dispatcher.add_handler(CommandHandler(ci.name, ci.func))
                regdhelp[ci.name] = cmd
                if ci.alias != None:
                    dispatcher.add_handler(CommandHandler(ci.alias, ci.func))
                    regdhelp[ci.alias] = cmd
                    logging.info("Registered command /{}, /{}".format(ci.name, ci.alias))
                else:
                    logging.info("Registered command /{}".format(ci.name))
            elif ci.type == CommandType.Schedule:
                to_schedule.append(ci)
            else:
                dispatcher.add_handler(MessageHandler(ci.filter, ci.func))
                logging.info("Registered monitor {}".format(ci.name))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    logging.info("Started polling for commands.")
    if len(to_schedule) > 0:
        logging.info("Registering scheduled tasks..")
    for ci in to_schedule:
        ci.func(updater)
        logging.info("Registered scheduled task {}".format(ci.name))

def load_config(filename):
    global baseconf
    global translator
    global commands
    conf = dict()
    with open(filename, 'r') as f:
        conf = yaml.load(f)
    baseconf = conf["base"]
    logging.info("Loaded base configuration.")
    for command in _commands.__all__:
        if 'Command' not in command and command not in baseconf['disabled_modules']:
            mod = importlib.import_module('commands')
            commands.append(getattr(mod, command)(logging))
        elif command in baseconf['disabled_modules']:
            logging.info("Disabled module {}.".format(command))
    for cmd in commands:
        section = "command.{}".format(cmd.safename)
        if section in conf.keys():
            cmd.load_config(conf[section])
    logging.info("Loaded module configurations.")
        
if __name__ == "__main__":
    parser  = argparse.ArgumentParser()
    parser.add_argument("--config", help="configuration file to use", type=str)
    args = parser.parse_args()
    if os.path.exists(args.config):
        load_config(args.config)
        main()
    else:
        logging.error("No config file found.")
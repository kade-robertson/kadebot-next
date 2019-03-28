#!/usr/bin/env python

import argparse
import logging
import os

import configbetter
from telegram.ext import MessageHandler, Updater

from .config import AppConfig

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def setup_bot(args):
    pass


def main():
    appdirs = configbetter.Config('kadebot')
    appdirs.makedirs()
    config = AppConfig(os.path.join(appdirs.config, 'config.ini'))

    parser = argparse.ArgumentParser(description='kadebot - Telegram chat bot, using message intent to improve chat')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help='Path to your config.ini, if not placed in the default location ($XDG_CONFIG_HOME/kadebot/config.json)')
    args = parser.parse_args()
    setup_bot(args)


if __name__ == '__main__':
    main()

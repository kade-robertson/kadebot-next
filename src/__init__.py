#!/usr/bin/env python

import argparse
import logging
import os

import configbetter
from telegram.ext import MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
conf = configbetter.Config('kadebot-next')


def setup_bot(args):
    pass


def main():
    conf.makedirs()
    parser = argparse.ArgumentParser(description='kadebot - Telegram chat bot, using message intent to improve chat')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help=
        f'Path to your config.json, if not placed in the default location ({os.path.join(conf.config, "config.json")})')
    args = parser.parse_args()
    setup_bot(args)


if __name__ == '__main__':
    main()

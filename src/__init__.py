#!/usr/bin/env python

import argparse
import logging

from telegram.ext import Updater, MessageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def setup_bot(args):
    pass


def main():
    parser = argparse.ArgumentParser(description='kadebot - Telegram chat bot, using message intent to improve chat')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help='Path to your config.json, if not placed in the default location ($XDG_CONFIG_HOME/kadebot/config.json)')
    parser.parse_args()
    setup_bot(args)


if __name__ == '__main__':
    main()

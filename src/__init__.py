#!/usr/bin/env python

import argparse
import logging
import os
import sys

import configbetter
from telegram.ext import MessageHandler, Updater

from .config import AppConfig

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def setup_bot(args: argparse.Namespace, config: AppConfig):
    pass


def main():
    appdirs = configbetter.Config('kadebot')
    appdirs.makedirs()
    config_path = os.path.join(appdirs.config, 'config.ini')

    parser = argparse.ArgumentParser(description='kadebot - Telegram chat bot, using message intent to improve chat')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help=f'Path to your config.ini, if not placed in the default location ({config_path})')
    args = parser.parse_args()

    if args.config:
        config_path = args.config
    config = AppConfig(config_path)

    if not config.valid:
        print(
            'The config file provided ({}) was not valid. Ensure you have an api_key in the [kadebot] section.',
            file=sys.stderr)
        sys.exit(1)

    print(type(args))
    setup_bot(args, config)


if __name__ == '__main__':
    main()

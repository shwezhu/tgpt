#!/usr/bin/env python

import click
import config
from cli import start_talk
from models import Bots


@click.command()
@click.option("-b", "--bot", "bot", type=click.STRING, help="Set bot which will set the cheapest model for the specified bot, available choices: gpt.")
@click.option("-m", "--multiline", "multiline", is_flag=True, help="Use the multiline input mode.")
@click.option("-t", "--translator", "translator", is_flag=True, help="Use the translator mode, just select one mode in a conversation.")
@click.option("-r", "--reader", "reader", is_flag=True, help="Use the reader mode, just select one mode in a conversation.")
def main(bot, multiline, translator, reader):
    conf = config.load_config("../config.yaml")

    # parsing config from cli, will override the previous loaded config if exists.
    if bot in Bots:
        conf["model"] = Bots[bot]
    conf["multiline"] = multiline
    # only one mode can be selected.
    if translator:
        conf["translator"] = True
    elif reader:
        conf["reader"] = True

    if conf["multiline"]:
        print("Multiline mode, input prompt ending twice twice Enter, type Ctrl+C to end conversion: ")
    else:
        print("Normal mode, type 'quit' or 'exit' to end conversion: ")

    start_talk(conf)


if __name__ == "__main__":
    main()

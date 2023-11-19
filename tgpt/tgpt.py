#!/usr/bin/env python

import click
import gpt
import config


@click.command()
@click.option("-m", "--model", "model", type=click.STRING, help="Set the model")
@click.option(
    "-mt", "--max_tokens", "max_tokens", type=click.INT, help="Set the maximum number of tokens to generate within a "
                                                              "response of chatGPT"
)
@click.option(
    "-ml", "--multiline", "multiline", is_flag=True, help="Use the multiline input mode"
)
def main(model, max_tokens, multiline):
    conf = config.load_config("../config.yaml")
    if model is not None:
        conf["model"] = model
    if max_tokens is not None:
        conf["max_tokens"] = max_tokens
    conf["multiline"] = multiline

    if conf["multiline"]:
        print("Input prompt ending with an empty line: ")
    else:
        print("Ask any questions (type 'quit' or 'exit' to exit): ")
    gpt.start_talk(conf)


if __name__ == "__main__":
    main()

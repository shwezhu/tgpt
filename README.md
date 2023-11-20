# tgpt

![Go HTTP file server pages](tgpt.gif)

## Overview

A simple python script for chatting with ChatGPT from the command line, using the official API.

## Installation

```shell
git clone git@github.com:shwezhu/tgpt.git
cd tgpt
pip install -r requirements.txt
```

Add the OpenAI API key to your `.bashrc` file in the root of your home folder (`.zshrc` if you use zsh).

```shell
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

## Usage

```shell
cd tgpt
./tgpt.py
# python3 ./tgpt.py -ml  # multiple line mode
# python3 ./tgpt.py -mt 300 # specify max_tokens
```

> Make sure the script executable: `chmod +x tgpt.py`

```shell
❯ ./tgpt.py --help
Usage: tgpt.py [OPTIONS]

Options:
  -m, --model TEXT           Set the model
  -mt, --max_tokens INTEGER  Set the maximum number of tokens to generate
                             within a response of chatGPT
  -ml, --multiline           Use the multiline input mode
  --help                     Show this message and exit.
```
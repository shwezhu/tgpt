import rich
import openai
from openai import OpenAI
from rich.prompt import Prompt

console = rich.console.Console()

client = OpenAI()
messages = []

GPT4 = "gpt-4-1106-preview"
GTP3Dot5 = "gpt-3.5-turbo"
MAX_TOKENS = 300


def handle_stream(response):
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()


def gpt(config: dict) -> None:
    """
    Makes stream request.
    :return: None
    """
    model = GTP3Dot5
    max_tokens = MAX_TOKENS
    if "model" in config:
        model = config["model"]
    if "max_tokens" in config:
        max_tokens = config["max_tokens"]

    try:
        r = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            max_tokens=max_tokens
        )
    # https://platform.openai.com/docs/guides/error-codes/api-errors
    except openai.APIError as e:
        messages.pop()
        print(f"OpenAI API returned an API Error: {e.message}")
        return
    except openai.RateLimitError as e:
        messages.pop()
        print(f"OpenAI API request exceeded rate limit: {e.message}")
        return
    except Exception as e:  # capture any other exceptions and raise it.
        messages.pop()
        console.print(f"An error occurred: {e}", style="red bold")
        return

    handle_stream(r)


def start_talk(config: dict) -> None:
    while True:
        try:
            query = Prompt.ask("[yellow]ask any questions (type 'quit' to exit)[/yellow]")
        # Ctrl + C will raise KeyboardInterrupt, command + D will raise EOFError on macOS
        except (EOFError, KeyboardInterrupt):
            rich.print("\n")
            exit()
        if query.lower() == "quit":
            exit()
        if query == "":
            continue

        messages.append({"role": "user", "content": query})
        gpt(config)

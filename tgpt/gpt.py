import openai
from openai import OpenAI
from message import messages
import message
import cost
import prompt


client = OpenAI()


def start_talk(config: dict) -> None:
    tryMarkdown(config)
    while True:
        if config["multiline"]:
            msg = prompt.with_multiline()
        else:
            msg = prompt.with_line()

        if msg is None:
            exit()
        if msg.strip() == "":
            continue

        message.with_user(msg)
        gpt(config)


def gpt(config: dict) -> None:
    """
    Makes stream request.
    """
    model, max_tokens = getParas(config)

    # https://platform.openai.com/docs/guides/error-codes/api-errors
    try:
        r = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            # This limits the maximum number of tokens to generate in the chat completion, not all tokens in the
            # context.
            max_tokens=max_tokens,
        )
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
        print(f"An error occurred: {e}")
        return

    handle_stream(r, model)


def handle_stream(response, model: str):
    chunks = []
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            chunk = chunk.choices[0].delta.content
            print(chunk, end="", flush=True)
            chunks.append(chunk)
    print("\n")

    message.with_assistant(''.join(chunks))
    cost.display_expense(messages, model)


def getParas(config: dict):
    """
    Parse model and max_tokens in dict config, if not found in config dict, use model "gpt-3.5-turbo-1106"
    and 'None' for max_tokens.
    """
    model = config.get("model", "gpt-3.5-turbo-1106")
    max_tokens = config.get("max_tokens", None)
    return model, max_tokens


def tryMarkdown(config: dict):
    if config.get("markdown", False):
        message.add_markdown()

import rich
import openai
import tiktoken
from openai import OpenAI
from rich.prompt import Prompt
from system import messages
import system

console = rich.console.Console()
client = OpenAI()
prompt_tokens = 0
completion_tokens = 0


def start_talk(config: dict) -> None:
    tryMarkdown(config)
    while True:
        try:
            query = Prompt.ask("[yellow]ask any questions (type 'quit' or 'exit' to exit)[/yellow]")
        # Ctrl + C will raise KeyboardInterrupt, command + D will raise EOFError on macOS
        except (EOFError, KeyboardInterrupt):
            print("\n")
            exit()
        if query.lower() == "quit" or query.lower() == "exit":
            exit()
        if query == "":
            continue

        messages.append({"role": "user", "content": query})
        gpt(config)


def gpt(config: dict) -> None:
    """
    Makes stream request.
    :return: None
    """
    model, max_tokens = getParas(config)

    # https://platform.openai.com/docs/guides/error-codes/api-errors
    try:
        r = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            max_tokens=max_tokens
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
        console.print(f"An error occurred: {e}", style="red bold")
        return

    handle_stream(r)


def handle_stream(response):
    chunks = []
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            chunk = chunk.choices[0].delta.content
            print(chunk, end="", flush=True)
            chunks.append(chunk)

    messages.append({"role": "assistant", "content": "".join(chunks)})
    update_tokens()


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
        system.add_markdown()


def update_tokens() -> None:
    global prompt_tokens  # the message sent to chatgpt
    global completion_tokens  # the generated response
    prompt_tokens = num_tokens_from_messages(messages[:len(messages) - 1])
    completion_tokens = num_tokens_from_messages([messages[len(messages)-1]])


def num_tokens_from_messages(msgs, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        # print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        # print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai
            -python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )

    num_tokens = 0
    for message in msgs:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))

    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

from rich.prompt import Prompt
import message
import assistant
from cost import display_expense
from animation import Animation
import rich


def start_talk(config: dict) -> None:
    bot = assistant.Assistant(config)

    try_markdown(config)
    try_select_mode(config)
    while True:
        if config["multiline"]:
            msg = with_multiline()
        else:
            msg = with_line()

        if msg is None:
            exit()
        if msg.strip() == "":
            continue

        message.with_user(msg)
        handle_stream(bot.chat(message.messages), bot.provider.model, config.get("interactive", False))


def handle_stream(response_iter, model: str, interactive: bool) -> None:
    # Start loading animation
    animation = Animation()
    animation.start()

    chunks = []
    try:
        for chunk in response_iter:
            if animation.is_alive():
                animation.stop()  # Stop and clear animation
                rich.print(f"[bold green]{model}: [/bold green]", end="")
            print(chunk, end="", flush=True)
            chunks.append(chunk)
    except KeyboardInterrupt:
        exit()
    print("\n")

    message.with_assistant(''.join(chunks))
    display_expense(message.messages, model)

    # not chat history sending back to bot, if interactive mode is not enabled.
    if not interactive:
        message.trim_last_two_messages()


def try_markdown(config: dict):
    if config.get("markdown", False):
        message.add_markdown()


def try_select_mode(config: dict):
    if config.get("translator", False):
        message.translator_mode()
    elif config.get("reader", False):
        message.reader_mode()


def with_multiline() -> str | None:
    prompt = []
    try:
        line = Prompt.ask("[bold yellow]You[/bold yellow]")
    except (EOFError, KeyboardInterrupt):
        return None
    while line:
        prompt.append(line)
        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            return None

    return "\n".join(prompt)


def with_line() -> str | None:
    try:
        line = Prompt.ask("[bold yellow]You[/bold yellow]")
    # Ctrl + C will raise KeyboardInterrupt, command + D will raise EOFError on macOS
    except (EOFError, KeyboardInterrupt):
        return None
    if line.lower() == "quit" or line.lower() == "exit":
        return None
    return line

from rich.prompt import Prompt
from message import messages
import message
import assistant
from cost import display_expense
from animation import Animation
import rich


def start_talk(config: dict) -> None:
    bot = assistant.Assistant(config)

    tryMarkdown(config)
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
        handle_stream(bot.chat(messages), bot.provider.model)


def handle_stream(response_iter, model: str):
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
    display_expense(messages, model)


def tryMarkdown(config: dict):
    if config.get("markdown", False):
        message.add_markdown()


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

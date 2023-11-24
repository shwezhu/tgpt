from message import messages
import message
import assistant
import input
from cost import display_expense
from animation import Animation
import rich


def start_talk(config: dict) -> None:
    bot = assistant.Assistant(config)

    tryMarkdown(config)
    while True:
        if config["multiline"]:
            msg = input.with_multiline()
        else:
            msg = input.with_line()

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

from typing import TypedDict


class Message(TypedDict):
    role: str
    content: str


messages = []


def with_system(msg: str) -> None:
    """
    Add a system message to the message list.
    """
    messages.append({"role": "system", "content": msg})


def with_user(msg: str) -> None:
    """
    Add a user message to the message list.
    """
    messages.append({"role": "user", "content": msg})


def with_assistant(msg: str) -> None:
    """
    Add an assistant message to the message list.
    """
    messages.append({"role": "assistant", "content": msg})


def add_markdown() -> None:
    """
    Try to force ChatGPT to always respond with well formatted code blocks and tables if markdown is enabled.
    """
    instruction = ("Always use code blocks with the appropriate language tags. If asked for a table always format it "
                   "using Markdown syntax.")
    with_system(instruction)

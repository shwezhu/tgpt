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
    instruction = "Always use code blocks with the appropriate language tags. If asked for a table always format it using Markdown syntax."
    with_system(instruction)


def translator_mode() -> None:
    """
    Try to force ChatGPT act as an English translator, spelling corrector and improver.
    """
    instruction = "I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations."
    with_system(instruction)


def reader_mode() -> None:
    """
    Add a reader mode message to the message list.
    """


def trim_last_two_messages() -> None:
    global messages
    if len(messages) > 2:
        messages = messages[:-2]

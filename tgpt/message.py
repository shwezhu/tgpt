messages = []


def add_markdown() -> None:
    """
    Try to force ChatGPT to always respond with well formatted code blocks and tables if markdown is enabled.
    """
    instruction = ("Always use code blocks with the appropriate language tags. If asked for a table always format it "
                   "using Markdown syntax.")
    messages.append({"role": "system", "content": instruction})


def with_user(msg: str) -> None:
    messages.append({"role": "user", "content": msg})


def with_assistant(msg: str) -> None:
    messages.append({"role": "assistant", "content": msg})

PRICING_RATE = {
    "gpt-3.5-turbo": {"prompt": 0.001, "completion": 0.002},
    "gpt-3.5-turbo-1106": {"prompt": 0.001, "completion": 0.002},
    "gpt-3.5-turbo-0613": {"prompt": 0.001, "completion": 0.002},
    "gpt-3.5-turbo-16k": {"prompt": 0.001, "completion": 0.002},
    "gpt-4": {"prompt": 0.03, "completion": 0.06},
    "gpt-4-0613": {"prompt": 0.03, "completion": 0.06},
    "gpt-4-32k": {"prompt": 0.06, "completion": 0.12},
    "gpt-4-32k-0613": {"prompt": 0.06, "completion": 0.12},
    "gpt-4-1106-preview": {"prompt": 0.01, "completion": 0.03},
}


messages = []


def add_markdown() -> None:
    """
    Try to force ChatGPT to always respond with well formatted code blocks and tables if markdown is enabled.
    """
    instruction = ("Always use code blocks with the appropriate language tags. If asked for a table always format it "
                   "using Markdown syntax.")
    messages.append({"role": "system", "content": instruction})

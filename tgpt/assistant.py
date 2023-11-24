from typing import List, Iterator
from openai_completion import OpenAICompletionProvider
from message import Message
from completion import CompletionProvider


def get_completion_provider(model: str) -> CompletionProvider:
    if model.startswith("gpt"):
        return OpenAICompletionProvider(model)
    else:
        raise ValueError(f"Unknown model: {model}")


class Assistant:
    def __init__(self, config: dict):
        self.config = config
        self.provider = get_completion_provider(config["model"])

    def chat(self, messages: List[Message]) -> Iterator[str]:
        return self.provider.complete(messages, self.config)

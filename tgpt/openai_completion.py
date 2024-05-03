from typing import Iterator, cast, Any
import openai
from rich import print
from openai import OpenAI
from completion import CompletionProvider


class OpenAICompletionProvider(CompletionProvider):
    def __init__(self, model: str):
        self.client = OpenAI()
        self.model = model

    def complete(self, messages: list, args: dict, stream: bool = True) -> Iterator[str]:
        kwargs = {}
        if "max_tokens" in args:
            kwargs["max_tokens"] = args["max_tokens"]
        if "temperature" in args:
            kwargs["temperature"] = args["temperature"]

        try:
            r = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream,
                **kwargs,
            )
        except openai.APIError as e:
            messages.pop()
            print(f"OpenAI API returned an API Error: {e.message}")
            return iter([])
        except openai.RateLimitError as e:
            messages.pop()
            print(f"OpenAI API request exceeded rate limit: {e.message}")
            return iter([])
        except Exception as e:  # capture any other exceptions and raise it.
            messages.pop()
            print(f"An error occurred: {e}")
            return iter([])

        response_iter = cast(Any, r)

        if stream:
            for response in response_iter:
                if response.choices[0].delta.content is not None:
                    chunk = response.choices[0].delta.content
                    yield chunk
        else:
            yield response_iter.choices[0].message.content

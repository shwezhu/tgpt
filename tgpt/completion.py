from abc import abstractmethod
from typing import List, Iterator
from message import Message


class CompletionProvider:
    @abstractmethod
    def complete(
            self,
            messages: List[Message],
            args: dict,
            stream: bool = True
    ) -> Iterator[str]:
        """
        Makes request to the provider, stream=True by default.
        """
        pass

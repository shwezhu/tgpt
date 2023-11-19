import logging

import tiktoken
from rich.logging import RichHandler

from models import PRICING_RATE

logger = logging.getLogger("rich")

prompt_tokens = 0
completion_tokens = 0


def display_expense(messages: list, model: str) -> None:
    update_tokens(messages, model)

    logger.info(
        f"\nTotal tokens used: [green bold]{prompt_tokens + completion_tokens}",
        extra={"highlighter": None},
    )

    if model in PRICING_RATE:
        total_expense = calculate_expense(
            prompt_tokens,
            completion_tokens,
            PRICING_RATE[model]["prompt"],
            PRICING_RATE[model]["completion"],
        )
        logger.info(
            f"Estimated expense: [green bold]${total_expense}",
            extra={"highlighter": None},
        )
    else:
        logger.warning(
            f"[red bold]No expense estimate available for model {model}",
            extra={"highlighter": None},
        )


def calculate_expense(
        _prompt_tokens: int,
        _completion_tokens: int,
        prompt_pricing: float,
        completion_pricing: float,
) -> str:
    expense = ((_prompt_tokens / 1000) * prompt_pricing) + (
            (_completion_tokens / 1000) * completion_pricing
    )
    expense = "{:.6f}".format(round(expense, 6))

    return expense


def update_tokens(messages: list, model: str) -> None:
    global prompt_tokens  # the message sent to chatgpt
    global completion_tokens  # the generated response
    prompt_tokens += num_tokens_from_messages(messages[:len(messages) - 1], model)
    completion_tokens = num_tokens_from_messages([messages[len(messages) - 1]], model)


def num_tokens_from_messages(messages: list, model: str) -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning(
            "Warning: model not found. Using cl100k_base encoding.",
            extra={"highlighter": None},
        )
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0
    for message in messages:
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4
        for key, value in message.items():
            assert isinstance(value, str)
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

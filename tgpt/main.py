from openai import OpenAI

GPT4 = "gpt-4-1106-preview"
GTP3Dot5 = "gpt-3.5-turbo"
MAX_TOKENS = 100

client = OpenAI()


def gpt(model, messages, max_tokens=MAX_TOKENS):
    """
    gpt sends request to ChatGPT, according to the model and messages provided.
    :return: the responded message and the tokens used in this chat.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )
    return completion.choices[0].message, completion.usage.total_tokens


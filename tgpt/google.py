import os

import requests
from rich.prompt import Prompt

from completion import CompletionProvider

google_base_endpoint = "https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{MODEL}"

config = {
    "region": "us-central1",
    "project_id": "gemini-test-408215",
    "model": "gemini-pro:streamGenerateContent",
}

api_key = os.environ.get("GOOGLE_API_KEY")

headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {api_key}",
}

contents = []

request_body = {
    "contents": contents,
    "safetySettings": [
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        }
    ],
    "generation_config": {
        "temperature": 0.4,
        "topP": 1.0,
        "topK": 32,
        "maxOutputTokens": 1000,
    }
}


def append_user_text_to_contents(text: str) -> None:
    return contents.append({
        "role": "user",
        "parts": [{"text": text, }]
    })


def append_bot_text_to_contents(text: str) -> None:
    return contents.append({
        "role": "model",
        "parts": [{"text": text, }]
    })


class GoogleBot(CompletionProvider):
    def __init__(self, model: str, region: str, project_id: str):
        self.model = model
        self.url = google_base_endpoint.format(REGION=region, PROJECT_ID=project_id, MODEL=model)

    def complete(self, messages: list, args: dict, stream: bool = True):

        pass


def main():
    while True:
        try:
            line = Prompt.ask("[bold yellow]You[/bold yellow]")
        # Ctrl + C will raise KeyboardInterrupt, command + D will raise EOFError on macOS
        except (EOFError, KeyboardInterrupt):
            break
        if line.lower() == "quit" or line.lower() == "exit":
            break
        append_user_text_to_contents(line)
        try:
            r = requests.post(
                google_base_endpoint.format(REGION=config["region"], PROJECT_ID=config["project_id"], MODEL=config["model"]),
                headers=headers,
                json=request_body,
            )
        except Exception as e:
            print(e)
            contents.pop()
            break
        if r.status_code == 200:
            print(r.content)
            print(r.json())
            response = r.json()
            #append_bot_text_to_contents(response["completionResult"]["text"])
            print(response)
        else:
            print(r.status_code)
            print(r.content)
            contents.pop()
            break


if __name__ == "__main__":
    main()

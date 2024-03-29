import json
import os
from abc import abstractmethod
import openai
import roastmate.constants as Constants


class LlmClient:
    @abstractmethod
    async def query(self, prompt: str) -> str:
        """ Receives a prompt and returns an answer"""


class OpenAiClient(LlmClient):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def query(self, prompt: str) -> str:
        print("PROMPT")
        print(prompt)
        response = await openai.ChatCompletion.acreate(
            api_key=self.api_key,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(response.__dict__)
        return response.choices[0].message['content']

    @classmethod
    def default(cls) -> 'OpenAiClient':
        return OpenAiClient(api_key=parse_api_key())


def parse_api_key() -> str:
    if os.getenv(Constants.OPENAI_API_KEY):
        api_key = json.loads(os.getenv(Constants.OPENAI_API_KEY))['api-key']
    else:
        with open("secrets/openai.json", "r") as f:
            api_key = json.loads(f.read())['api-key']
    return api_key

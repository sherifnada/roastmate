import json

from aiohttp import ClientSession


class SendBlue:
    def __init__(self, api_key: str, api_secret, client_session: ClientSession):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client_session = client_session

    async def send_imessage_text(self, group_id: str, content: str):
        async with self.client_session.post(
                "https://api.sendblue.co/api/send-group-message",
                json={
                    'group_id': group_id,
                    'content': content
                },
                headers={
                    "SB-API-KEY-ID": self.api_key,
                    "SB-API-SECRET-KEY": self.api_secret
                }
        ) as response:
            # TODO handle status_callbacks
            response.raise_for_status()
            return await response.json()

    @classmethod
    def init(cls, client: ClientSession) -> 'SendBlue':
        with open("secrets/sendblue.json", "r") as f:
            # TODO
            creds = json.loads(f.read())
            return SendBlue(creds['api_key'], creds['api_secret'], client)

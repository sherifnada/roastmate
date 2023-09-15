from aiohttp import ClientSession

import roastmate.constants as Constants
from roastmate.sendblue_client import SendBlue
import asyncio


async def send():
    async with ClientSession() as session:
        sb = SendBlue.init(session)
        # await sb.send_imessage_dm('+18023494963', media_url="https://picsum.photos/200/300.jpg")
        await sb.send_imessage_dm('+18023494963', media_url=Constants.VCARD_URL)

asyncio.run(send())
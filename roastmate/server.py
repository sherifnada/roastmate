from datetime import datetime
import random
from typing import Optional, List

import aiohttp
from aiohttp import ClientSession

from sanic import Sanic, Request
from sanic.response import text
from sanic.exceptions import SanicException

from roastmate.db_client import DbClient
from roastmate.sendblue_client import SendBlue

app = Sanic("Roastmate")
db_client = DbClient.prod()


@app.listener('before_server_start')
def init(app, loop):
    app.ctx.aiohttp_session = aiohttp.ClientSession(loop=loop)
    app.ctx.sendblue = SendBlue.init(app.ctx.aiohttp_session)


@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.ctx.aiohttp_session.close())
    loop.close()


@app.get("/")
async def hello_world(request: Request):
    return text("Hello, world.")


@app.post("/receive_message")
async def receive(request: Request):
    # TODO validate body schema
    # TODO handle non-group messages
    body = request.json
    group_id = body.get('group_id', None)

    if not group_id:
        raise SanicException("We can only do group messages right now. Booooo.", status_code=400)

    message_properties = parse_message(group_id, body)
    if group_id and await is_known_group(group_id):
        await save_message(**message_properties)
        # TODO generate quippy response
        message = await generate_quippy_response([])
        await app.ctx.sendblue.send_imessage_text(group_id, message)
        return text(f"We have seen group {group_id} before")
    else:
        await insert_known_group(group_id)
        await save_message(**message_properties)
        welcome_message = await generate_welcome_message()
        await app.ctx.sendblue.send_imessage_text(group_id, welcome_message)
        return text("Officer I've never seen this group before")


### utils
def parse_message(group_id: str, request_body: dict) -> dict:
    """
    # TODO this is stupid. Use an ORM or some request body validation.
    Raises SanicException if the message is invalid
    """
    content = request_body.get('content')
    sender = request_body.get('from_number')
    date_sent = datetime.strptime(request_body.get('date_sent'), '%Y-%m-%dT%H:%M:%S.%fZ')
    if content and sender and date_sent:
        return {
            'group_id': group_id,
            'content': content,
            'sender': sender,
            'date_sent': date_sent,
            'date_received': datetime.now()
        }
    else:
        raise SanicException(
            'Expected content, sender, and date_updated to be set for a group message webhook',
            status_code=400
        )


async def generate_welcome_message() -> str:
    welcome_messages = [
        "new phone who dis?",
        "I'm Roastmate, the digital dose of sass and wit you didn't know you needed. Buckle up buckaroos, it's roastin' time.",
    ]
    return welcome_messages[random.randrange(len(welcome_messages))]


async def generate_quippy_response(previous_messages: [List[str]]) -> Optional[str]:
    # TODO only respond sometimes
    return "Hello! I'm Roastmate. I'm still cooking. And soon, you will too!"


### DB OPS
# TODO make it a class
async def is_known_group(group_id: str) -> bool:
    groups = (await db_client.query("SELECT * FROM imessage_group WHERE id=:group_id;", {'group_id': group_id})).fetchall()
    return len(groups) > 0


async def save_message(group_id: str, content: str, sender: str, date_sent: datetime, date_received: datetime):
    await db_client.query(
        "INSERT INTO group_message(group_id, content, sender, date_sent, date_received) VALUES (:group_id, :content, :sender, :date_sent, "
        ":date_received)",
        {'group_id': group_id, 'content': content, 'sender': sender, 'date_sent': date_sent, 'date_received': date_received}
    )


async def insert_known_group(group_id: str):
    await db_client.query("INSERT INTO imessage_group(id) VALUES (:group_id);", {'group_id': group_id})

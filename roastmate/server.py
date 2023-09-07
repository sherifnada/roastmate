from datetime import datetime
import random
from typing import Optional, List, Mapping

import aiohttp

from sanic import Sanic, Request
from sanic.response import text
from sanic.exceptions import SanicException

from roastmate import strings
from roastmate.db_client import DbClient
from roastmate.llm_client import OpenAiClient
from roastmate.prompts import get_group_message_roast_prompt, get_name_saved_prompt
from roastmate.sendblue_client import SendBlue
from roastmate.types import TextMessage, SenderRole, Contact

app = Sanic("Roastmate")
db_client = DbClient.prod()


@app.listener('before_server_start')
def init(app, loop):
    app.ctx.aiohttp_session = aiohttp.ClientSession(loop=loop)
    app.ctx.sendblue = SendBlue.init(app.ctx.aiohttp_session)
    app.ctx.llm = OpenAiClient.default()


@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.ctx.aiohttp_session.close())
    loop.close()


@app.post("/receive_message")
async def receive(request: Request):
    # TODO validate body schema
    # TODO handle non-group messages
    # TODO ask for first_name
    body = request.json
    group_id = body.get('group_id', None)
    from_number = body['from_number']
    print(body)
    # Sender role is always USER since we are receiving the message
    message_properties = parse_message(group_id, body) | {'sender_role': SenderRole.USER}
    if group_id:
        # TODO enrich all participant messages not just the one sending the message
        message_properties['sender_name'] = await get_contact_name(from_number)
        if await is_known_group(group_id):
            await save_message(**message_properties)
            previous_messages = await get_previous_group_messages(group_id)
            message = await generate_quippy_response(previous_messages)
            await save_message(group_id, message, "+11234567890", datetime.utcnow(), datetime.utcnow(), "Roastmate", SenderRole.LLM)
            await app.ctx.sendblue.send_imessage_group_text(group_id, message)
            return text(f"We have seen group {group_id} before")
        else:
            await insert_known_group(group_id)
            await save_message(**message_properties)
            await app.ctx.sendblue.send_imessage_group_text(group_id, strings.GROUP_WELCOME_MESSAGE)

            convo_participants = body.get("participants", [])
            await create_contacts_from_numbers(convo_participants)
            await request_group_participant_details(convo_participants)

            return text("Officer I've never seen this group before")
    elif body.get("content", "").lower().startswith("roastmate please"):
        rest_of_text = body.get("content")[len("roastmate please"):].lstrip()
        if rest_of_text.lower().startswith("call me"):
            name = rest_of_text[len("call me"):].lstrip()
            await set_contact_name(from_number, name)
            response_message = await generate_name_saved_response(name)
            await app.ctx.sendblue.send_imessage_dm(from_number, response_message)
            return text("success")
        else:
            # Unknown command
            pass
    else:
        # TODO direct, non-command DMs
        pass
        # if imessage:
        # else:


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
            'sender_number': sender,
            'date_sent': date_sent,
            'date_received': datetime.now(),
        }
    else:
        raise SanicException(
            'Expected content, sender, and date_updated to be set for a group message webhook',
            status_code=400
        )


async def request_group_participant_details(numbers: List[int]):
    # TODO track if we already know these contacts, and if we've already asked them for their numbers and how many times
    for number in numbers:
        await app.ctx.sendblue.send_imessage_dm(number, strings.DM_WELCOME_MESSAGE)


### LLM OPS
async def generate_name_saved_response(name: str) -> str:
    prompt = get_name_saved_prompt(name)
    return await app.ctx.llm.query(prompt)


async def generate_quippy_response(previous_messages: [List[TextMessage]]) -> Optional[str]:
    # TODO only respond sometimes
    # TODO handle very long texts
    prompt = get_group_message_roast_prompt(previous_messages)
    response = await app.ctx.llm.query(prompt)
    if response.startswith("Roastmate:"):
        response = response[len("Roastmate:"):].lstrip()
    return response


### DB OPS
# TODO make it a class
async def is_known_group(group_id: str) -> bool:
    groups = (await db_client.query("SELECT * FROM imessage_group WHERE id=:group_id;", {'group_id': group_id})).fetchall()
    return len(groups) > 0


async def save_message(
        group_id: str,
        content: str,
        sender_number: str,
        date_sent: datetime,
        date_received: datetime,
        sender_name: str = None,
        sender_role: SenderRole = SenderRole.USER
):
    await db_client.query(
        "INSERT INTO group_message(group_id, content, sender_number, sender_name, date_sent, date_received, sender_role) "
        "VALUES (:group_id, :content, :sender_number, :sender_name, :date_sent, :date_received, :sender_role)",
        {
            'group_id': group_id,
            'content': content,
            'sender_number': sender_number,
            'sender_name': sender_name,
            'date_sent': date_sent,
            'date_received': date_received,
            'sender_role': sender_role.value
        }
    )


async def insert_known_group(group_id: str):
    await db_client.query("INSERT INTO imessage_group(id) VALUES (:group_id);", {'group_id': group_id})


async def get_previous_group_messages(group_id: str, limit=5) -> List[TextMessage]:
    messages = (await db_client.query(
        f"""
        SELECT sender_number, sender_name, content
        FROM group_message
        WHERE group_id=:group_id 
        ORDER BY date_sent DESC 
        LIMIT {limit};
        """,
        {'group_id': group_id}
    )).fetchall()

    return [TextMessage(sender_number=x[0], sender_name=x[1], content=x[2]) for x in messages]


async def create_contacts_from_numbers(numbers: List[str]):
    if len(numbers) == 0:
        return

    variables = {str(i): number for i, number in enumerate(numbers)}
    values = ",".join([f"(:{i})" for i in range(len(numbers))])

    await db_client.query(f"""
        INSERT INTO contact(number) VALUES {values}    
    """, variables=variables)


async def set_contact_name(number: str, name: str):
    await db_client.query("""
    UPDATE contact SET name=:name WHERE number=:number;
    """, {'name': name, 'number': number})


async def get_contact_name(number: str) -> Optional[str]:
    contact = await get_single_contact(number)
    if contact:
        return contact.first_name


async def get_single_contact(number: str) -> Optional[Contact]:
    """
    returns number to contact
    """
    contacts = (await db_client.query(
        f"""
        SELECT number, name 
        FROM contact 
        WHERE number=:number
        """,
        variables={'number': number}
    )).fetchall()

    if len(contacts) == 1:
        return Contact(number=contacts[0][0], first_name=contacts[0][1])

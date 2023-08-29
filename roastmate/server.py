from sanic import Sanic, Request
from sanic.response import text

from roastmate.db_client import DbClient

db_client = DbClient.prod()
app = Sanic("MyHelloWorldApp")


@app.get("/")
async def hello_world(request: Request):
    print(await db_client.query("hello"))
    return text("Hello, world.")


@app.post("/receive_message")
async def receive(request: Request):
    # print()
    return text("Hello, world")

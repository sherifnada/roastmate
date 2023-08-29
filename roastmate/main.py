from sanic import Sanic, Request
from sanic.response import text

app = Sanic("MyHelloWorldApp")


@app.post("/")
async def hello_world(request: Request):
    print(request.json)
    return text("Hello, world.")

@app.post("/receive_message")
async def receive(request: Request):
    # print()
    return text("Hello, world")

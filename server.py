import asyncio
import aioredis
import uvloop
import sanic
from sanic.response import file

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = sanic.Sanic(__name__)
loop = asyncio.new_event_loop()


@app.route('/')
async def index(request):
    return await file('ws-test.html')


async def send(ws):
    redis = await aioredis.create_redis('redis://localhost/0')
    while True:
        data = await ws.recv()
        redis.publish_json('chan:1', data)


async def receive(ws):
    redis = await aioredis.create_redis('redis://localhost/0')
    channel = (await redis.subscribe('chan:1'))[0]
    while await channel.wait_message():
        msg = await channel.get_json()
        await ws.send(msg)


@app.websocket('/join')
async def join(request, ws):
    await asyncio.gather(send(ws), receive(ws))


if __name__ == '__main__':
    try:
        import sys
        port = sys.argv[1]
    except IndexError:
        port = 8000
    app.run(host="0.0.0.0", port=port, debug=True)

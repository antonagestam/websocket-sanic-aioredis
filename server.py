import asyncio
import aioredis
import uvloop
import sanic

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = sanic.Sanic(__name__)
loop = asyncio.get_event_loop()


@app.route('/')
async def index(request):
    return await file('ws-test.html')


async def publish(ws):
    """Receive messages from the WebSocket and pass them on to redis"""
    redis = await aioredis.create_redis('redis://localhost/0')
    while True:
        data = await ws.recv()
        await redis.publish_json('chan:1', data)


async def subscribe(ws):
    """Receive messages from redis and pass them on to the WebSocket"""
    redis = await aioredis.create_redis('redis://localhost/0')
    channel = (await redis.subscribe('chan:1'))[0]
    while await channel.wait_message():
        msg = await channel.get_json()
        await ws.send(msg)


@app.websocket('/join')
async def join(request, ws):
    """For every request we start a publish loop and a subscribe loop"""
    await asyncio.gather(publish(ws), subscribe(ws))


if __name__ == '__main__':
    try:
        import sys
        port = sys.argv[1]
    except IndexError:
        port = 8000
    app.run(host="0.0.0.0", port=port, debug=True)

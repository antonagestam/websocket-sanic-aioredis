# websocket-sanic-aioredis

## Setup

```sh
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
$ brew install redis && brew services start redis
# you can now run two different sanic processes, both talking to redis
$ python server.py 8001
```

Open two browser windows, open the console and type in `ws.send('hello');` in
one of them to see your message pop up in the other.

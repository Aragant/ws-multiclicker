import asyncio
import json
import secrets

from websockets.server import serve

GAME = {}

async def play(websocket):
    pass

async def handler(websocket):
    message = await websocket.recv()
    print(message)
    event = {
        "type": "login",
        "message": "OK",
    }
    await websocket.send(json.dumps(event))
    
    
    

async def main():
    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
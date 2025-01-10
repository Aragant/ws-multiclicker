import asyncio
import json
import secrets

from multiclicker import Multiclicker
from websockets.server import serve

GAME = {}

async def broadcast(connected, message):
    for websocket in connected.copy():  # Crée une copie pour éviter les erreurs de modification
        try:
            await websocket.send(message)
        except Exception:
            connected.remove(websocket)  # Supprimez le WebSocket fermé


async def play(websocket, game, connected):
    async for message in websocket:
        event = json.loads(message)
        if event["type"] == "click":
            game.click_increment()
        
            event = {
                "type": "clicked",
                "sumClick": game.click
                }
            await broadcast(connected, json.dumps(event))

            

async def handler(websocket):
    game, connected = GAME[0]
    
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "login"
    
    user_data = {}
    
    if "username" in event:
        user_data["username"] = event["username"]
        user_data["websocket"] = websocket
        user_data["sumClick"] = 0
    
    connected.add(websocket)
    
    event = {
        "type": "login",
        "message": "OK",
    }
    await websocket.send(json.dumps(event))
    
    await play(websocket, game, connected)
    
    
    

async def main():
    game = Multiclicker()
    connected = set()
    
    GAME[0] = game, connected
    
    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
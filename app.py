import asyncio
import json
import secrets 

# imported function 
from websocket_service.broadcast import broadcast

# imported enum 
from event.event_type import EventType
from event.event_key import EventKey
from event.event_value import EventValue
from event.event_factory import event_factory
from game.player import Player

from game.multiclicker import Multiclicker
from websockets import serve

GAME = {}
PLAYER = {}

async def play(game, websocket_id):
    game.score_increment()
    PLAYER[websocket_id].score_increment()

    event = event_factory(
        EventType.CLICKED,
        **{EventKey.SUMSCORE: game.sumScore},
        player={
            "username": PLAYER[websocket_id].username,
            "sumScore": PLAYER[websocket_id].sumScore
        }
    )
    print(event)
    return event

async def setClans(clanName):
    PLAYER[websocket_id].clan = clan
    print(PLAYER[websocket_id])
    
    clans = list(set(player.clan for player in PLAYER.values()))
    if clan not in clans:
        
    event = event_factory(
        EventType.SET_CLANS,
        player={
            "username": PLAYER[websocket_id].username,
            "clan": PLAYER[websocket_id].clan
        }
    )
    return event

async def joinClan(websocket_id, clan):
    PLAYER[websocket_id].clan = clan
    print(PLAYER[websocket_id])
        
    event = event_factory(
        EventType.JOIN_CLAN,
        player={
            "clan": PLAYER[websocket_id].clan
        }
    )
    return event
            

async def handler(websocket):
    game, connected = GAME[0]
    websocket_id = id(websocket) 
    
    message = await websocket.recv()
    event = json.loads(message)
    print(event)
    assert event[EventKey.TYPE] == EventType.LOGIN
    
    
    
    connected.add(websocket)
    PLAYER[id(websocket)] = Player(event[EventValue.USERNAME])
    
    event = event_factory(
        EventType.LOGIN,
        **{EventKey.MESSAGE: EventValue.OK}
        )
    await websocket.send(json.dumps(event))
    
    
    players = [ { "username": player.username, "sumScore": player.sumScore, "clan": player.clan } for player in PLAYER.values() ]
    # ca serais moin couteux de declarer un variable clans que l on incremente mais clan va sans doute decaler sur une api
    clans = [ { "clan": clan, "players": [player.username for player in PLAYER.values() if player.clan == clan] } for clan in set([player.clan for player in PLAYER.values()]) ]
    event = event_factory(
        EventType.GET_GAME_INFO, 
        game={
            "sumScore": game.sumScore,
            # on pourrais rennomer player score en players
            "playerScore": players,
            "clans": clans
        }
    )
    
    print(event)
    
    await websocket.send(json.dumps(event))
    
    async for message in websocket:
        event = json.loads(message)
        if event[EventKey.TYPE] == EventType.CLICK:
            response_event = await play(game, websocket_id)
            await broadcast(connected, json.dumps(response_event))
        elif event[EventKey.TYPE] == EventType.JOIN_CLAN:
            print( event)
            response_event = await joinClan(websocket_id, event[EventKey.CLAN_NAME])
            await broadcast(connected, json.dumps(response_event))

async def main():
    game = Multiclicker()
    connected = set()
    
    GAME[0] = game, connected
    
    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
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

async def play(websocket, game, connected):
    async for message in websocket:
        event = json.loads(message)
        if event[EventKey.TYPE] == EventType.CLICK:
            game.score_increment()
            PLAYER[id(websocket)].score_increment()

            event = event_factory(
                EventType.CLICKED,
                **{EventKey.SUMSCORE: game.sumScore},
                player={
                    "username": PLAYER[id(websocket)].username,
                    "sumScore": PLAYER[id(websocket)].sumScore,
                },
            )
            print(event)
            await broadcast(connected, json.dumps(event))


async def handler(websocket):
    game, connected = GAME[0]

    message = await websocket.recv()
    event = json.loads(message)
    print(
        "---------------------------------------------------------------------------------------------------------"
    )
    print(event)
    print(
        "---------------------------------------------------------------------------------------------------------"
    )

    assert event[EventKey.TYPE] == EventType.LOGIN

    connected.add(websocket)
    PLAYER[id(websocket)] = Player(event[EventValue.USERNAME])

    event = event_factory(EventType.LOGIN, **{EventKey.MESSAGE: EventValue.OK})
    await websocket.send(json.dumps(event))

    players = [
        {"username": player.username, "sumScore": player.sumScore}
        for player in PLAYER.values()
    ]
    event = event_factory(
        EventType.GET_GAME_INFO,
        game={"sumScore": game.sumScore, "playerScore": players},
    )

    print(event)

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

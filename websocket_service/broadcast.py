async def broadcast(connected, message):
    for websocket in connected.copy():  # Crée une copie pour éviter les erreurs de modification
        try:
            await websocket.send(message)
        except Exception:
            connected.remove(websocket)  # Supprimez le WebSocket fermé
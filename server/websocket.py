import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send('{"version":"2.8","features":"[]"}')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 9002))
asyncio.get_event_loop().run_forever()

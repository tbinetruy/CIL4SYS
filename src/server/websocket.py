import asyncio
import websockets
import json



async def echo(websocket, path):
    a = 1
    async for message in websocket:
        if a == 1:
            await websocket.send('{"version":"2.8","features":"[]"}')
            a = 2
        elif a == 2:
            await websocket.send('{"name":"sentValues","value":[{"name":"trafficLight","type":"string","value":[{"name":"state","value":"green"}]}]}')
            a = 3
        else:
            await websocket.send('{"name":"sentValues","value":[{"name":"trafficLight","type":"string","value":[{"name":"state","value":"red"}]}]}')
            a = 2


#async def echo(websocket, path):
#    async for message in websocket:
#        print("Receiving request", message)
#        req = json.loads(message)
#        resp = 0
#
#
#        if req["name"] == "modelInfos":
#            resp = json.dumps({
#                "version": "2.8",
#                "features": [],
#            })
#        else:
#            resp = '{"name":"sentValues","value":[{"name":"trafficLight","type":"string","value":[{"name":"state","value":"green"}]}]}'
#            #json.dumps({
#                #"action": [1],
#
#        import pdb; pdb.set_trace()
#        await websocket.send(resp)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 9002))
asyncio.get_event_loop().run_forever()

import json
import asyncio
import logging
from utils import uniqid, timestamp
from aiodriver.aiologin import login

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)


async def main(gameworld):
    with open(r'/home/didadadida93/Desktop/cred.json', 'r') as f:
        cred = json.load(f)

    driver = await login(cred['email'], cred['password'], gameworld)

    url = (
        driver.api_endpoint[:-5]
        + 'chat/socket.io/?ESO=3&'
        + 'transport=polling&'
        + f't={timestamp()}'
        + '-0'
    )
    await driver.client.get(url)

    for cookie in driver.client.session.cookie_jar:
        if cookie.key == 't5-game-io':
            sid = cookie.value

    url = (
        'wss'
        + driver.api_endpoint[5:-5]
        + 'chat/socket.io/?ESO=3&'
        + 'transport=websocket&'
        + f'sid={sid}'
    )

    async with driver.client.session.ws_connect(url) as ws:

        # Probing
        await ws.send_str('2probe')
        response = await ws.receive()
        if response:
            await ws.send_str('5')
        else:
            exit(0)  # TODO: Implement exceptions

        packet_number = 421
        payload = [
            "subscribe",
            {
                "playerId": str(driver.player_id),
                "uniqueClientIdentifier": uniqid(),
                "session": driver.session
            }
        ]
        payload = f'{packet_number}{json.dumps(payload)}'

        await ws.send_str(payload)
        response = await ws.receive()

    await driver.client.close()

if __name__ == '__main__':
    asyncio.run(main(gameworld='com7'))

from aiodriver.aiolobby import Lobby

async def login(email, password, gameworld_name):
	driver = Lobby()

	await driver.authenticate(email, password)

	caches = await driver.post(
		action='get',
		controller='cache',
		params={
			'names': ['Collection:Avatar']
		}
	)

	for avatar in caches:
		if gameworld_name == avatar.worldName.lower():
			gameworld_id = avatar.consumersId
			break

	gameworld = await driver.connect_to_gameworld(g_name=gameworld_name, g_id=gameworld_id)

	caches = await gameworld.post(
		action='get',
		controller='cache',
		params={
			'names': ['Collection:Village:own']
		}
	)

	for data in caches:
		gameworld.player_id = data.playerId
		break

	return gameworld

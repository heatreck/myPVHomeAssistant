import asyncio

from api import MyPVClient

HOST = "192.168.178.146"
PASSWORD = "DEIN_PASSWORT"


async def main():
    client = MyPVClient(HOST, PASSWORD)

    print("Geräteinfo:")
    info = await client.get_info()
    print(info)

    print("\nLaufzeitdaten:")
    runtime = await client.get_runtime()
    print(runtime)

    print("\nLogin:")
    success = await client.login()
    print(success)

    print("\nSetup:")
    setup = await client.get_setup()
    print(setup)

    await client.close()


asyncio.run(main())

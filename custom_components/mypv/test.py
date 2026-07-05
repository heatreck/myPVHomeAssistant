import asyncio

from api import MyPVClient


async def main():

    client = MyPVClient(
        host="192.168.178.154",
        password="DEINPASSWORT",
    )

    print(await client.get_info())

    print(await client.get_runtime())

    print(await client.login())

    print(await client.get_setup())


asyncio.run(main())

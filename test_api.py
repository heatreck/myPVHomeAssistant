import asyncio
import json

from mypv_api.client import MyPVClient


HOST = "192.168.178.154"
PASSWORD = "SecureHome32?!"

async def main():

    client = MyPVClient(
        HOST,
        PASSWORD,
    )

    print(await client.login())

    print("Runtime:")
    runtime = await client.get_runtime()
    print(json.dumps(runtime, indent=4))
    print("Info:")
    info = await client.get_info()
    print(json.dumps(info, indent=4))
    setup = await client.get_setup()
    print("Setup:")
    print(json.dumps(setup, indent=4))

    await client.close()


asyncio.run(main())
from __future__ import annotations
from urllib import response
from urllib.parse import quote_plus
from urllib.parse import quote


import aiohttp
import asyncio
import ssl

from aiohttp import ClientTimeout


class MyPVClient:

    def __init__(
        self,
        host: str,
        password: str | None = None,
        timeout: int = 5,
    ):

        self.host = host
        self.password = password

        self.timeout = ClientTimeout(total=timeout)

        self._setup_cache = None

        self._ssl = ssl.create_default_context()
        self._ssl.check_hostname = False
        self._ssl.verify_mode = ssl.CERT_NONE

        self.session = aiohttp.ClientSession(
    timeout=self.timeout,
    connector=aiohttp.TCPConnector(
        ssl=self._ssl,
    ),
)

    # Start Request

    async def request(
        self,
        protocol: str,
        method: str,
        endpoint: str,
        data=None,
        allow_redirects=True,
    ):
        session = self.session

        if protocol == "https":
            session = self.session

        url = f"{protocol}://{self.host}/{endpoint}"

        headers = {
        "Origin": f"https://{self.host}",
        "Referer": f"https://{self.host}/",
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",


    }
        
        print("DATA:", repr(data))
        print("TYPE:", type(data))


        async with session.request(
            method,
            url,
            data=data,
            headers=headers,
            allow_redirects=allow_redirects,
        ) as response:
            
            print(f"{method} {url}")
            print(f"Status: {response.status}")
            print(f"Content-Type: {response.content_type}")
            print("REQUEST HEADERS:")
            print(response.request_info.headers)

            if response.content_type == "application/json":
                return await response.json()
            return await response.text()

    # Runtime
    async def get_runtime(self) -> dict:
        return await self.request(
            "http",
            "GET",
            "data.jsn",
        )

    # Device info
    async def get_info(self) -> dict:
        return await self.request(
            "http",
            "GET",
            "mypv_dev.jsn",
        )

    # Authentication
    async def login(self):
        if self.password is None:
            raise RuntimeError("Password missing")

        payload = self.password.replace("?", "%3F") 
        payload = "pw=" + payload

        print(repr(payload))

        await asyncio.sleep(2)

        auth_response = await self.request(
            "https",
            "POST",
            "auth.jsn",
            data=payload,
        )

        print("POST Response:")
        print(auth_response)

        await asyncio.sleep(2)

#        payload = {
#            "fsetup": "0",
#            "pw": self.password
#        }
#        
#        await self.request(
#            "https",
#            "POST",
#            "setup.jsn",
#            data=payload,
#        )

        auth = await self.request(
            "https",
            "GET",
            "auth.jsn",
        )

        print(auth)

        return auth["auth"] == 1


    # Setup
    async def get_setup(self) -> dict:
        if self._setup_cache:
            return self._setup_cache

        await self.login()

        self._setup_cache = await self.request(
            "https",
            "GET",
            "setup.jsn",
        )

        return self._setup_cache

    # Set Parameters
    async def set_parameter(
        self,
        parameter,
        value,
    ):
        setup = await self.get_setup()
        setup[parameter] = value
        await self.post_setup(setup)

    # post Setup
#    async def post_setup(
#        self,
#        setup,
#    ):
#        setup["pw"] = self.password
#
#        await self.request(
#            "https",
#            "POST",
#            "setup.jsn",
#            data=setup,
#        )

        self._setup_cache = setup

    async def close(self):
        await self.session.close()

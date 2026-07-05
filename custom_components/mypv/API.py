from __future__ import annotations

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

        self.http = aiohttp.ClientSession(
            timeout=self.timeout
        )

        self.https = aiohttp.ClientSession(
            timeout=self.timeout,
            connector=aiohttp.TCPConnector(
                ssl=self._ssl
            ),
        )

// Start Request
  async def request(

    self,

    protocol: str,

    method: str,

    endpoint: str,

    data=None,

    allow_redirects=True,

):

    session = self.http

    if protocol == "https":
        session = self.https

    url = f"{protocol}://{self.host}/{endpoint}"

    async with session.request(

        method,

        url,

        data=data,

        allow_redirects=allow_redirects,

    ) as response:

        if response.content_type == "application/json":
            return await response.json()

        return await response.text()

//Runtime

async def get_runtime(self):

    return await self.request(

        "http",

        "GET",

        "data.jsn",

    )

// Device info
async def get_info(self):

    return await self.request(

        "http",

        "GET",

        "mypv_dev.jsn",

    )

// Authentication
async def login(self):

    if self.password is None:
        raise RuntimeError("Password missing")

    payload = {

        "pw": self.password

    }

    await self.request(

        "https",

        "POST",

        "auth.jsn",

        data=payload,

    )

    auth = await self.request(

        "https",

        "GET",

        "auth.jsn",

    )

    return auth["auth"] == 1

// Setup 

async def get_setup(self):

    if self._setup_cache:

        return self._setup_cache

    await self.login()

    self._setup_cache = await self.request(

        "https",

        "GET",

        "setup.jsn",

    )

    return self._setup_cache

// Set Parameters 

async def set_parameter(

    self,

    parameter,

    value,

):

    setup = await self.get_setup()

    setup[parameter] = value

    await self.post_setup(setup)

// post Setup

async def post_setup(

    self,

    setup,

):

    setup["pw"] = self.password

    await self.request(

        "https",

        "POST",

        "setup.jsn",

        data=setup,

    )

    self._setup_cache = setup


async def close(self):
    await self.http.close()
    await self.https.close()

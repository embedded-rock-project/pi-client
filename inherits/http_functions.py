"""
Rocco Ahching
25 August 2021
Embedded Programming
Aiohttp session setup for asyncronhous requests.
"""


import aiohttp
import asyncio

from typing import Any, Optional
from config import server_base_url, discord_base_url


class RequestMaker:
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop if loop else asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self._nowait = self.loop.create_task
        self.session = self._await(self.create_session())

    # unsafe behavior.
    def __del__(self):
        try:
            self._await(self.session.close())
        except Exception as e:
            print(e)


    async def create_session(self, **kwargs) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(**kwargs)

    async def server_report(self, endpoint: str, payload: Any) -> str:
        async with self.session.post(url=server_base_url + endpoint, json=payload) as req:
            return await req.text()

    async def discord_report(self, **kwargs) -> str:
        async with self.session.post(url=discord_base_url, **kwargs) as req:
            return await req.text()

    # for daniel
    def request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        return self._await(self.session.request(method, url, **kwargs))

    def handle_request_text(self, request: aiohttp.ClientResponse) -> str:
        return self._await(request.text())

    def handle_request_json(self, request: aiohttp.ClientResponse) -> dict:
        return self._await(request.json())


    # for not daniel
    async def async_request(self, method: str, url: str, **kwargs) -> str:
        async with self.session.request(method, url, **kwargs) as req:
            return await req.text()

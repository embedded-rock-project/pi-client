"""
Rocco Ahching
25 August 2021
Embedded Programming
Aiohttp session setup for asyncronhous requests.
"""


from urllib.request import Request
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


    def __del__(self):
        try:
            self._await(self.session.close())
        except Exception:
            pass


    async def create_session(self, **kwargs) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(**kwargs)

    async def server_report(self, endpoint: str, payload: Any) -> str:
        async with self.session.post(url=server_base_url + endpoint, json=payload) as req:
            return await req.text()

    def discord_report(self, **kwargs) -> str:
        return self.request("POST", discord_base_url, **kwargs)
        #return self.request("POST", "https://httpbin.org/ip", **kwargs)

    # for daniel
    def request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        return self._await(self.session.request(method, url, **kwargs))

    # sync get text from original request.
    # Usage: rm.req_text(rm.request("GET", "https://google.com"))
    def req_text(self, request: aiohttp.ClientResponse) -> str:
        return self._await(request.text())

    # sync get serialized JSON from original request.
    # Usage: rm.req_json(rm.request("GET", "https://google.com"))
    def req_json(self, request: aiohttp.ClientResponse) -> dict:
        return self._await(request.json())


    # for not daniel
    # Literally same functionality as above except can be excecuted asynchronously.
    async def async_request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        return await self.session.request(method, url, **kwargs)


defaultMaker = RequestMaker()
"""
Rocco
25 August 2021
Embedded Programming
Aiohttp session setup for asyncronhous requests.
"""
import nest_asyncio
nest_asyncio.apply()


import aiohttp
import asyncio

from typing import Any, Optional
from config import server_base_url, discord_base_url
import json


class RequestMaker:

    # Initialization
    #sets up request structure including image streaming, websocket connection, and event flag waiting loop
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop if loop else asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self._nowait = self.loop.create_task
        self.session: aiohttp.ClientSession = self._await(self.create_session())
        self.ws_server_connection: aiohttp.ClientWebSocketResponse = self._await(self.session.ws_connect(server_base_url+ "/pi", timeout=5))
        self.ws_image_feed: aiohttp.ClientWebSocketResponse = self._await(self.session.ws_connect(server_base_url + "/pi_camera_feed", timeout=5))
            
    # cleans up aiohttp clientSession (required)
    def __exit__(self, exc_type, exc_value, traceback):
        self._await(self.session.close())

    # manually close requestMaker.
    def close(self):
        self._await(self.ws_image_feed.send_str("disconnect_request"))
        self._await(asyncio.sleep(1))
        self.__exit__(None, None, None)

    # create aiohttp ClientSession (required to make async calls)
    async def create_session(self, **kwargs) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(**kwargs)
   
    #server logs to http website
    async def async_http_server_report(self, endpoint: str, payload: Any) -> str:
        async with self.session.post(url=server_base_url + endpoint, json=payload) as req:
            return await req.text()

    # Unused.
    def http_server_report(self, endpoint: str, **kwargs) -> str:
        return self.request("POST", server_base_url + endpoint, **kwargs)

    #server logs to discord
    def discord_report(self, **kwargs) -> str:
        return self.request("POST", discord_base_url, **kwargs)

    # base request that discord/server requests are based on.
    def request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        return self._await(self.session.request(method, url, **kwargs))
 

    # Same functionality as above except can be excecuted asynchronously.
    async def async_request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        return await self.session.request(method, url, **kwargs)

    # sync get text from original request.
    # Usage: rm.req_text(rm.request("GET", "https://google.com"))
    def req_text(self, request: aiohttp.ClientResponse) -> str:
        return self._await(request.text())

    # sync get serialized JSON from original request.
    # Usage: rm.req_json(rm.request("GET", "https://google.com"))
    def req_json(self, request: aiohttp.ClientResponse) -> dict:
        return self._await(request.json())

    # report to server via established websocket.
    def ws_server_report(self, sensor: str, type: str, message: Any, **kwargs):
        data = {"sensor": sensor, "type": type, "message": message, **kwargs}
        self._await(self.ws_server_connection.send_json(data))

    # send binary image data over websocket.
    def ws_img_feed_send(self, data: Any, **kwargs):
        self._await(self.ws_image_feed.send_bytes(data))
    
    # async generator for "as completed" messages from the server.
    async def ws_server_listen(self):
        while True:
            yield await self.ws_server_connection.receive()






defaultMaker = RequestMaker()

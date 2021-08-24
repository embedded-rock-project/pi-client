import aiohttp


from typing import Any
from config import server_base_url, discord_base_url


def test():
    return "hi"







async def server_report(session: aiohttp.ClientSession, endpoint: str, payload: Any) -> str:
    async with session.post(url=server_base_url + endpoint , json=payload) as req:
        return await req.text()




async def discord_report(session: aiohttp.ClientSession, **kwargs) -> str:
    async with session.post(url=discord_base_url, **kwargs) as req:
        return await req.text()


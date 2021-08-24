import aiohttp
import asyncio

from typing import Any
from config import server_base_url, discord_base_url



async def test() -> aiohttp.ClientSession:
    return aiohttp.ClientSession()


async def server_report(session: aiohttp.ClientSession, endpoint: str, payload: Any) -> str:
    async with session.post(url=server_base_url + endpoint , json=payload) as req:
        return await req.text()


async def discord_report(session: aiohttp.ClientSession, **kwargs) -> str:
    async with session.post(url=discord_base_url, **kwargs) as req:
        return await req.text()


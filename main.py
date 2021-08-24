"""
Client side interactions with sensors and server.
All interactions must be handled inside the code itself, 
then data is handed off to a server to process.
"""


import asyncio
import aiohttp
from typing import Optional
import helper
import config





class RaspberryPiClient:

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop if loop else asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self._nowait = self.loop.create_task
        self.session = self._await(self.create_session())


    async def create_session(self, **kwargs) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(**kwargs)


def main(): 
    rm = RaspberryPiClient()
    emb = helper.build_embed("hi", fields=(("hi", None)))
    emb_json = helper.embeds_to_json(emb)
    print(emb_json)
    rm._await(helper.discord_report(rm.session, json={"content": None, "embeds": emb_json}))
    return


if __name__ == "__main__":
    main()
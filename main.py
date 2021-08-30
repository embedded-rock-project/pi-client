"""
Client side interactions with sensors and server.
All interactions must be handled inside the code itself, 
then data is handed off to a server to process.
"""


import asyncio
import helper
from inherits import RequestMaker




def main():
    rm = RequestMaker()
    loop = asyncio.get_event_loop()
    emb = helper.build_embed("hi", fields=(("hi", "hi", False)))
    emb_json = helper.embeds_to_json(emb)
    resp = loop.run_until_complete(rm.discord_report(json={"content": None, "embeds": emb_json}))
    print(emb_json)
    print(resp)
    return



if __name__ == "__main__":
    main()

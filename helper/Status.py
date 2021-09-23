import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
randomizer=random.randint(0,5)
def zero():
  return "The rock has met rocco, he is unimpressed. "
def one():
  return  "The rock is feeling happy"
def two():
  return  "The rock is cooking"
def three():
  return  "The rock, although weathered, continues to rock"
def four():
  return  "The rock is looking for a worthy opponent, it has found none"
def five():
  return  "The rock has decided to play rock paper scissors, but has found no opponent"
def six():
  return  "The rock is currently trying to think of things to say, but to no avail, because it's a rock"
def seven():
  return  "The rock is fearful of potential threats, but with the power of the sparkles security system, he remains safe."
switcher = {
  0:zero,
  1:one,
  2:two,
  3:three,
  4:four,
  5:five
}
def switch(message):
  return switcher.get(message)()
@client.event
async def on_message(message):
  if message.author == client.user:
        return
  if message.content == ('!Status','!status'):
    response = switch(randomizer)
    await message.channel.send(response)

client.run(TOKEN)

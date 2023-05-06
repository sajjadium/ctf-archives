#!/usr/bin/env python3
import discord
import redis

from secret import *

DB_BOT = 1

client = discord.Client()

@client.event
async def on_ready():
    print(f"We've logged in as {client.user}")
    channel = client.get_channel(LOGGING_CHANNEL_ID)
    if channel is None:
        print("Failed to get channel...")
        exit(1)

    c = redis.Redis(host='redis', port=6379, db=DB_BOT)
    while True:
        r = c.blpop('report', 1)
        if r is not None:
            key, value = r
            try:
                await channel.send(value.decode())
            except Exception as e:
                print(f"[ERROR] {e}")

client.run(DISCORD_SECRET)

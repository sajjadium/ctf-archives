#############################################
# Author: Krishnan Navadia
# This is main working file for this chal
#############################################

import discord
from discord.ext import commands, tasks
import subprocess

from settings import ADMIN_ROLE
import os
from dotenv import load_dotenv
from time import time

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command('help')

SHELL_ESCAPE_CHARS = [":", "curl", "bash", "bin", "sh", "exec", "eval,", "|", "import", "chr", "subprocess", "pty", "popen", "read", "get_data", "echo", "builtins", "getattr"]

COOLDOWN = []

def excape_chars(strings_array, text):
    return any(string in text for string in strings_array)

def pyjail(text):
    if excape_chars(SHELL_ESCAPE_CHARS, text):
        return "No shells are allowed"

    text = f"print(eval(\"{text}\"))"
    proc = subprocess.Popen(['python3', '-c', text], stdout=subprocess.PIPE, preexec_fn=os.setsid)
    output = ""
    try:
        out, err = proc.communicate(timeout=1)
        output = out.decode().replace("\r", "")
        print(output)
        print('terminating process now')
        proc.terminate()
    except Exception as e:
        proc.kill()
        print(e)

    if output:
        return f"```{output}```"


@bot.event
async def on_ready():
    print(f'{bot.user} successfully logged in!')

@bot.command(name="flag", pass_context=True)
async def flag(ctx):
    admin_flag = any(role.name == ADMIN_ROLE for role in ctx.message.author.roles)

    if admin_flag:
        cmds = "Here are some functionalities of the bot\n\n`!add <number1> + <number2>`\n`!sub <number1> - <number2>`"
        await ctx.send(cmds)
    else:
        message = "Only 'admin' can see the flag.😇"
        await ctx.send(message)

@bot.command(name="add", pass_context=True)
async def add(ctx, *args):
    admin_flag = any(role.name == ADMIN_ROLE for role in ctx.message.author.roles)
    if admin_flag:
        arg = " ".join(list(args))
        user_id = ctx.message.author.id
        ans = pyjail(arg)
        if ans: await ctx.send(ans)
    else:
        await ctx.send("no flag for you, you are cheating.😔")

@bot.command(name="sub", pass_context=True)
async def sub(ctx, *args):
    admin_flag = any(role.name == ADMIN_ROLE for role in ctx.message.author.roles)
    if admin_flag:
        arg = " ".join(list(args))
        ans = pyjail(arg)
        if ans: await ctx.send(ans)
    else:
        await ctx.send("no flag for you, you are cheating.😔")


@bot.command(name="help", pass_context=True)
async def help(ctx, *args):
    await ctx.send("Try getting `!flag` buddy... Try getting flag.😉")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Try getting `!flag` buddy... Try getting flag.😉")
    else:
        print(f'Error: {error}')


bot.run(TOKEN)

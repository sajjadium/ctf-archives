import io
from os import environ
import time

import discord
from discord import ApplicationContext, option
from discord.ext import commands
from pyrate_limiter import BucketFullException, Duration, Limiter, RequestRate

limiter = Limiter(RequestRate(1, Duration.MINUTE), RequestRate(10, Duration.HOUR))

VIKECTF_DISCORD = 1065757344459411486
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


def is_organizer():
    async def auth(ctx: ApplicationContext) -> bool:
        if "Organizer" not in [r.name for r in ctx.user.roles]:
            msg = f"{ctx.user.mention}` is not in the sudoers file. This incident will be reported`"
            await ctx.respond(msg, ephemeral=True, delete_after=10)
            raise commands.MissingPermissions(msg)
        return True

    return commands.check(auth)


def rate_limit():
    async def ha(ctx: ApplicationContext) -> bool:
        try:
            limiter.try_acquire(ctx.user.id)
        except BucketFullException as err:
            remaining_time = int(err.meta_info.get("remaining_time"))
            msg = f"{ctx.user.mention} has hit the request limit. Next request available <t:{ int(time.time()) + remaining_time}:R>"
            await ctx.respond(msg, delete_after=remaining_time - 1, ephemeral=True)
            raise commands.CommandInvokeError(msg)
        return True

    return commands.check(ha)


@bot.slash_command()
@option(
    "channel_id",
    description="Enter the channel ID to export",
)
@is_organizer()
@rate_limit()
async def export(ctx: ApplicationContext, channel_id: str):
    try:
        channel = ctx.bot.get_channel(int(channel_id))
        if not channel or channel.guild.id != VIKECTF_DISCORD:
            await ctx.respond("Channel not in vikeCTF discord", ephemeral=True, delete_after=10)
            return
    except Exception as e:
        print(e)
        await ctx.respond("Invalid channel ID", ephemeral=True, delete_after=10)
        return

    messages = await channel.history(limit=3).flatten()
    formatted_messages = "\n".join([f"```{discord.utils.remove_markdown(message.clean_content)}```" for message in messages])

    await ctx.respond(formatted_messages, ephemeral=True)

@export.error
async def on_application_command_error(
    ctx: discord.ApplicationContext, error: discord.DiscordException
):
    if isinstance(error, commands.CommandInvokeError):
        print(f"RateLimit: {error.original}")
    elif isinstance(error, commands.MissingPermissions):
        print(f"PermissionError: {error.missing_permissions}")
    elif isinstance(error, discord.errors.ApplicationCommandInvokeError) and "Missing Access" in str(error):
        await ctx.respond("Dont have permissions to view channel", ephemeral=True, delete_after=10)
    else:
        await ctx.respond("Error", ephemeral=True, delete_after=10)
        raise error


bot.run(environ.get("TOKEN"))

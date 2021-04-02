import logging
import os
import random

import discord
from dotenv import load_dotenv
from zalgo_text import zalgo

load_dotenv()
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX") or "!zalgo"
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
EASTER_EGGS = ("HE COMES", "HE RISES", "HE AWAKENS")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)
client = discord.Client()
zalgofier = zalgo.zalgo()


@client.event
async def on_ready():
    logging.info(f"Listening for command prefix: {COMMAND_PREFIX}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Prevent infinite loops
    elif has_mentions(message):
        await message.channel.send(zalgofier.zalgofy(random.choice(EASTER_EGGS)))
    elif message.content.startswith(COMMAND_PREFIX):
        await handle_command(message.channel, message.author, message.content)


def has_mentions(message):
    return (
        message.mention_everyone
        or len(message.mentions) > 0
        or len(message.channel_mentions) > 0
        or len(message.role_mentions) > 0
    )


async def handle_command(channel, member, command):
    logging.info(f"Handling command from: {member}: {command}")

    prefix, *rest = command.split(" ")
    if prefix != COMMAND_PREFIX:
        return  # Don't match !zalgoasdf

    if len(rest) == 0:
        await show_help(channel)
        return  # Catch bare prefix

    subcommand, *args = rest
    if subcommand == "nick" and len(args) > 0:
        await zalgofy_nickname(channel, member, " ".join(args))
    elif subcommand == "text" and len(args) > 0:
        await zalgofy_text(channel, " ".join(args))
    else:
        await show_help(channel)


async def zalgofy_nickname(channel, member, nickname):
    logging.info(f"Zalgofying nick for: {member}: {nickname}")
    zalgofied_nickname = zalgofier.zalgofy(nickname)
    await member.edit(nick=zalgofied_nickname)
    await channel.send("You have been blessed by Zalgo!")


async def zalgofy_text(channel, text):
    logging.info(f"Zalgofying text: {text}")
    await channel.send(zalgofier.zalgofy(text))


async def show_help(channel):
    logging.info(f"Showing help message")
    help = f"""
    Available commands:
    {COMMAND_PREFIX} nick foo
    {COMMAND_PREFIX} text bar
    """
    await channel.send(help)


client.run(DISCORD_TOKEN)

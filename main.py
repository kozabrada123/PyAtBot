import Settings
import atapi
import os
from embeds import server_info_embed, help_embed

import datetime
import time

import discord
from discord import app_commands
from discord.ext import tasks
import colorama

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print_out("Starting..", colorama.Fore.MAGENTA)
    status = "Starting.."

    await tree.sync(guild=discord.Object(id=Settings.GUILDID))
    await bot.change_presence(activity=discord.Activity(name=status,type=discord.ActivityType.watching))

    atapi.connect_account()

    keepAlive.start()
    updateStatus.start()

@tree.command(name="launch", description="Starts the server", guild=discord.Object(id=Settings.GUILDID))
async def launch(ctx):
    status = atapi.get_status()

    if status == "Offline":
        await ctx.response.send_message("Starting the server...")
        atapi.start_server()

        print("[" + datetime.datetime.now().strftime(
            "%H:%M:%S") + "]" + colorama.Fore.GREEN + " Server launched!" + colorama.Style.RESET_ALL)

        while True:
            if atapi.get_status() == "Online":
                await ctx.response.send_message(f"The server has started!")
                break


    elif atapi.get_status() == "Online":
        await ctx.response.send_message("The server is already online.")

    else:
        await ctx.response.send_message("Could not start the server. Reason: server is " + atapi.get_status())


@tree.command(name="status", description="Prints the server status", guild=discord.Object(id=Settings.GUILDID))
async def status(ctx):
    await ctx.response.send_message(embed=server_info_embed())


#async def helpcommand(ctx):
#    await ctx.send(embed=help_embed())


# T A S K S

@tasks.loop(seconds=10.0)
async def updateStatus():

    try:
        server_status = atapi.get_status()
    except:
        return;

    if server_status == "Online":

        players_num = atapi.get_players_num()

        if players_num == 0:

            text = f"| Online | " \
                   f"{atapi.get_time_left()} left | " \

        else:
            text = f"| Online | " \
                   f"{atapi.get_players_num()} | " \

    else:
        text = f"| {atapi.get_status()} | " \

    activity = discord.Activity(type=discord.ActivityType.watching, name=text)
    await bot.change_presence(activity=activity)


@tasks.loop(minutes=30)
async def keepAlive():
    atapi.refresh_browser()


def print_out(out, color):
    print("")
    print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "]" + color, out, colorama.Style.RESET_ALL)


# Run the bot
bot.run(Settings.TOKEN)
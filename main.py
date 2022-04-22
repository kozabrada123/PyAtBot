import Settings
import atapi
from embeds import server_info_embed, help_embed

import datetime
import time

import discord
import colorama
from discord.ext import tasks, commands



bot = discord.ext.commands.Bot(command_prefix=Settings.prefix,
                               description=Settings.description,
                               case_insensitive=True,
                               help_command=None)


@bot.event
async def on_ready():
    print_out("Starting..", colorama.Fore.MAGENTA)
    status = "Starting.."

    await bot.change_presence(activity=discord.Activity(name=status,type=discord.ActivityType.custom))

    atapi.connect_account()

    # Wait just to be sure
    time.sleep(3)

    # Start both tasks
    keepAlive.start()
    updateStatus.start()


@bot.command()
async def launch(ctx):
    status = atapi.get_status()

    if status == "Offline":
        await ctx.send("Starting the server...")
        atapi.start_server()

        author = ctx.author

        print("[" + datetime.datetime.now().strftime(
            "%H:%M:%S") + "]" + colorama.Fore.GREEN + " Server launched by " + colorama.Fore.CYAN + author.name,
              author.discriminator + colorama.Style.RESET_ALL)

        while True:
            time.sleep(5)
            if atapi.get_status() == "Online":
                await ctx.send(f"{author.mention}, the server has started!")
                break


    elif atapi.get_status() == "Online":
        await ctx.send("The server is already online.")

    else:
        await ctx.send("Could not start the server. Reason: server is " + atapi.get_status())


@bot.command()
async def status(ctx):
    await ctx.send(embed=server_info_embed())


@bot.command()
async def helpcommand(ctx):
    await ctx.send(embed=help_embed())


# T A S K S

@tasks.loop(seconds=10.0)
async def updateStatus():
    server_status = atapi.get_status()
    if server_status == "Online":
        text = f"| Online | " \
               f"{len(atapi.get_players())} | " \
               f"at.help"

    else:
        text = f"| {atapi.get_status()} | " \
               f"at.help"

    activity = discord.Activity(type=discord.ActivityType.custom, name=text)
    await bot.change_presence(activity=activity)


@tasks.loop(minutes=30)
async def keepAlive():
    atapi.refreshBrowser()


def print_out(out, color):
    print("")
    print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "]" + color, out, colorama.Style.RESET_ALL)


# Run the bot
bot.run(Settings.Token)
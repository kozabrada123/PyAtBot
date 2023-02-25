from discord import Embed
import Settings
import atapi

def server_info_embed():

    ip = atapi.get_ip()
    status = atapi.get_status()
    players_num = atapi.get_players_num()
    players = str(atapi.get_players()).replace('[', '').replace(']', '')
    tps = atapi.get_tps()
    ram = atapi.get_ram()
    software = atapi.get_software()
    version = atapi.get_version()

    if status == "Online":
        if players_num == 0:
            text = f"Ip: {ip}\n" \
                   f"Status: **{status}** \n" \
                   f"Number of players: {players_num} \n" \
                   f"Shutting down {atapi.get_discord_timestamp_from_time_left(atapi.get_time_left())} \n" \
                   f"Tps: {tps} \n" \
                   f"RAM: {ram} \n" \
                   f"Software: {software} \n" \
                   f"Version: {version} \n"
        else:
            text = f"Ip: {ip}\n" \
                   f"Status: **{status}** \n" \
                   f"Number of players: {players_num} \n" \
                   f"Player list: {players} \n" \
                   f"Tps: {tps} \n"\
                   f"RAM: {ram} \n"\
                   f"Software: {software} \n"\
                   f"Version: {version} \n"

    else:
        text = f"Ip: {ip}\n" \
               f"Status: **{status}** \n" \
               f"Software: {software} \n" \
               f"Version: {version} \n"

    embed = Embed()
    embed.add_field(name="Info for " + ip, value=text, inline=False)
    return embed


def help_embed():
    embed = Embed(title="Help")
    embed.add_field(name=Settings.prefix + "launch",
                    value="Launches the server",
                    inline=False)
    embed.add_field(name=Settings.prefix + "status",
                    value="Gives you all the info you need!")
    embed.add_field(name=Settings.prefix + "help",
                    value="Displays this message",
                    inline=False)
    return embed
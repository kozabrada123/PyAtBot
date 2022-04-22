from discord import Embed
import Settings
import atapi

def server_info_embed():

    text = f"**Ip:** {atapi.get_ip()} \n" \
           f"**Status:** {atapi.get_status()} \n" \
           f"**Number of players:** {len(atapi.get_players())} \n" \
           f"**Player list:** {str(atapi.get_players()).replace('[', '').replace(']', '')} \n" \
           f"**Software:** {atapi.get_software()} \n"\
           f"**Version:** {atapi.get_version()} \n" \

    embed = Embed()
    embed.add_field(name="Info for " + atapi.get_ip(), value=text, inline=False)
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
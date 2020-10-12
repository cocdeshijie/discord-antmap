import discord
import ast
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from fuzzywuzzy import process
from config import Config

config = Config()
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

file = open("./genus.json", "r")
contents = file.read()
genus_db = ast.literal_eval(contents)
file.close()
file = open("./species.json", "r")
contents = file.read()
species_db = ast.literal_eval(contents)
file.close()


@bot.command(name="map")
async def antmap(ctx, *, name):
    """Shows distribution map of <species> from antmaps.org."""
    if len(name.split(" ")) == 1:
        name = fuzzy_genus(name)
        embed = discord.Embed(title=display_name(name), description="https://antmaps.org/?mode=diversity&genus=" + name_to_map_url(name), color=0x3498db)
        embed.set_image(url=str(antmap_image_genus(name)))
        await ctx.send(embed=embed)
    else:
        name = fuzzy_search(name)
        embed = discord.Embed(title=display_name(name), description="https://antmaps.org/?mode=species&species=" + name_to_map_url(name), color=0x3498db)
        embed.set_image(url=str(antmap_image(name)))
        await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("This command cannot be left blank.")

# fuzzy search
def fuzzy_search(name):
    name = name.split()
    name_list = []
    name_list.append(process.extractOne(name[0], genus_db)[0])
    sp = species_db[name_list[0]]
    name_list.append(process.extractOne(name[1], sp)[0])
    return " ".join(name_list)

def fuzzy_genus(name):
    name = name.split()
    genus = process.extractOne(name[0], genus_db)[0]
    return genus

# change "camponotus frAgilis" to "Camponotus fragilis"
def display_name(name):
    if len(name) == 1:
        name = [item.lower() for item in name]
        name = "".join(name)
        return name.lower().title()
    else:
        name = name.split()
        name = [item.lower() for item in name]
        name[0] = name[0].title()
        return " ".join(name)

# change "camponotus frAgilis" to "Camponotus.fragilis"
def name_to_map_url(name):
    name = name.split()
    name = [item.lower() for item in name]
    name[0] = name[0].title()
    return " ".join(name).replace(" ", ".")

#antmap_url
def antmap_image(name):
    return "https://antmap.coc.tools/images/" + name_to_map_url(name) + ".png"

# antmap genus
def antmap_image_genus(name):
    return "https://antmap.coc.tools/images/" + name_to_map_url(name) + ".png"

bot.run(config.TOKEN)

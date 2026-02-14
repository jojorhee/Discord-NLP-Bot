import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from logging import FileHandler, DEBUG
from ollama import chat
import random
import csv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
GUILD_ID = discord.Object(id=1468366165041615112)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

handler = FileHandler(filename="discord.log", encoding="utf-8", mode="w")

#client = discord.Client(intents = discord.Intents.default())
client = commands.Bot(command_prefix="!", intents=intents)
#tree = app_commands.CommandTree(client)

joke_prompt = "Make a very funny, and short joke! It can be PG-13, and cursing is allowed, " \
" but it shouldn't be super inappropriate. Make it short enough that it can be a short " \
"message in discord! Only include the joke, nothing else, and make a unique one each time"

roles = ["Elite", "Peasant", "Gamer", "warner", "jack", "jojo"]

with open("shortjokes.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    data_list = []

    for row in reader:
        data_list.append(row)

'''@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(f"{client.user} is connected to the following guild:")
    print(f"{guild.name}(id: {guild.id})")

    members = '\n - '.join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")'''

@client.tree.command(name="hello", description="What's up fool?", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there 😉")

    try:
        guild = discord.Object(id=1468366165041615112)
        synced = await client.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to guild {guild.id}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@client.tree.command(name="help", description="erm, chat, what should I do", guild=GUILD_ID)
async def help(interaction: discord.Interaction):
    text = "Here are available commands: \n" \
    "/hello - greetings from a bot! \n" \
    "/joke - receive some laughter and joy \n" \
    ""
    await interaction.response.send_message(text)
    try:
        guild = discord.Object(id=1468366165041615112)
        synced = await client.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to guild {guild.id}")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@client.tree.command(name="joke", description="laughter's the best medicine...", guild=GUILD_ID)
async def joke(interaction: discord.Interaction):
    await interaction.response.send_message(data_list[random.randint(0, len(data_list) - 1)]["Joke"])

@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")
    await client.tree.sync(guild=GUILD_ID)

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hello {member.name}, welcome to the chat!"
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!99":
        pass
        #await message.channel.send("Testing")

    await client.process_commands(message)

@client.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@client.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=roles[0])
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {roles[0]}")
    else:
        await ctx.send("Role doesn't exist")

@client.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=roles[0])
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the role {roles[0]} removed")
    else:
        await ctx.send("Role doesn't exist")

@client.command()
@commands.has_role(roles[0])
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not has permission to do that")

@client.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@client.command()
async def reply(ctx):
    await ctx.reply("This is a reply to ur message")

@client.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("❤️")
    await poll_message.add_reaction("😘")



client.run(TOKEN, log_handler=handler, log_level=DEBUG)
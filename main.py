import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from logging import FileHandler, DEBUG

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

handler = FileHandler(filename="discord.log", encoding="utf-8", mode="w")

#client = discord.Client(intents = discord.Intents.default())
client = commands.Bot(command_prefix="!", intents=intents)

ro = "Elite"

'''@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(f"{client.user} is connected to the following guild:")
    print(f"{guild.name}(id: {guild.id})")

    members = '\n - '.join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")'''

@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")

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
    role = discord.utils.get(ctx.guild.roles, name=ro)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {ro}")
    else:
        await ctx.send("Role doesn't exist")

client.run(TOKEN, log_handler=handler, log_level=DEBUG)
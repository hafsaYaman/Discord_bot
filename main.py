import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token=os.getenv('DISCORD_TOKEN')
secret_role= "gamer"
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} has connected to discord!")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please watch your language!")
    
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role =discord.utils.get(ctx.guild.roles, name=secret_role)
    if role: 
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, you have been assigned the {secret_role} role")
    else:
        await ctx.send(f"Role {secret_role} not found.")

@bot.command()
async def remove(ctx):
    role =discord.utils.get(ctx.guild.roles, name=secret_role)
    if role: 
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention}, the {secret_role} role has been removed from you")
    else:
        await ctx.send(f"Role {secret_role} not found.")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send(f"{ctx.author.mention}, you have access to the secret command!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"{ctx.author.mention}, you do not have the required role to use this command.")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(msg)
    await ctx.send(f"you said {msg} in DM")    

@bot.command()
async def reply(ctx):
    await ctx.reply("this is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll", description=question, color=0x00ff00)
    poll_message= await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
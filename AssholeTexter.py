import discord
from discord.ext.commands import Bot
from discord.ext import commands
import config
import asyncio
import json
import time
import random
import os

#login
bot = discord.Client()
bot = commands.Bot(command_prefix='~at ')
bot.remove_command("help")
jsonList = []

#log in message
@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print('------')
    
async def createJsonFile(userID):
    userID = str(userID)
    #create a json file with the userID as the name
    #if the file already exists, do nothing
    if not os.path.exists(userID + '.json'):
        with open(userID + '.json', 'w') as f:
            json.dump({
                'userID': userID,
                'title': 'Hi I cannot come to the discord thing rn because i be asshole',
                'description': 'jk i just be busy asf rip',
                'emote': '',

            }, f)

@bot.command(aliases=['help','?'], name="Help",description="Help")
async def help(ctx):
    embeded = discord.Embed(title="Asshole Texter System Help", description="Get help on how to use the ATS")
    embeded.add_field(name="`~at add @User`", value="add user to the system", inline=False)
    embeded.add_field(name="`~at remove @User`", value="remove users from the system", inline=False)
    
    embeded.add_field(name="`~at title <Title>`", value="Change your title", inline=False)
    embeded.add_field(name="`~at desc <Description>`", value="Change your description", inline=False)
    embeded.add_field(name="`~at emote <Emote>`", value="Change your emote", inline=False)
    embeded.add_field(name="`~at list`", value="List all users in the system", inline=False)

    embeded.add_field(name="`~at help`", value="Get help on how to use the ATS", inline=False)
    await ctx.reply(embed=embeded)

@bot.command(aliases=['+','add'],name="Add",description="Add a user to the Asshole Texting System")
async def add(ctx, *, user: discord.Member):
    if(user.id in jsonList):
        embeded = discord.Embed(title=f"{user} is already part of the Asshole Texter System o~o", color=0x00ff00)
        embeded.set_thumbnail(url="https://cdn.discordapp.com/emojis/854451110307823626.gif?size=96")
        await ctx.reply(embed=embeded)
    else:
        jsonList.append(user.id)
        await createJsonFile(user.id)
        embeded = discord.Embed(title=f"{user} was added to the Asshole Texter System :3", color=0x00ff00)
        embeded.set_thumbnail(url="https://cdn.discordapp.com/emojis/900493142728540271.png?size=96")
        await ctx.reply(embed=embeded)

@bot.command(aliases=['-','remove'],name="Remove",description="Remove a user from the AssholeTexting System")
async def remove(ctx, *, user: discord.Member):
    if(user.id in jsonList):
        jsonList.remove(user.id)
        embeded = discord.Embed(title=f"{user} was removed from the Asshole Texter System ;-;", color=0x00ff00)
        embeded.set_thumbnail(url="https://cdn.discordapp.com/emojis/833529098122035232.png?size=96")
        await ctx.reply(embed=embeded)
    else:
        embeded = discord.Embed(title=f"{user} was not part of the Asshole Texter System to begin with", color=0x00ff00)
        embeded.set_thumbnail(url="https://cdn.discordapp.com/emojis/833529098122035232.png?size=96")
        await ctx.reply(embed=embeded)

@bot.command(aliases=['desc'], name="Description", description="Set the description of the message")
async def description(ctx, *, description):
    with open(str(ctx.author.id) + '.json', 'r') as file:
        data = json.load(file)
        data['description'] = description
        with open(str(ctx.author.id) + '.json', 'w') as file:
            json.dump(data, file)
        await ctx.reply("Description set")

@bot.command(aliases=['title'], name="Title", description="Set the title of the message")
async def title(ctx, *, title):
    with open(str(ctx.author.id) + '.json', 'r') as file:
        data = json.load(file)
        data['title'] = title
        with open(str(ctx.author.id) + '.json', 'w') as file:
            json.dump(data, file)
        await ctx.reply("Title set")

@bot.command(aliases=['emote'], name="Emote", description="Set the emote of the message")
async def emote(ctx, *, emote):
    with open(str(ctx.author.id) + '.json', 'r') as file:
        data = json.load(file)
        data['emote'] = emote
        with open(str(ctx.author.id) + '.json', 'w') as file:
            json.dump(data, file)
        await ctx.reply("Emote set")

@bot.command(aliases=['list'], name="List", description="List all users in the system")
async def list(ctx):
    embeded = discord.Embed(title="List of users in the Asshole Texter System", description="")
    for id in jsonList:
        user = await bot.fetch_user(id)
        embeded.add_field(name=user, value=id, inline=False)
    await ctx.reply(embed=embeded)

#On event
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    for id in jsonList:
        user = await bot.fetch_user(id)
        if user.mentioned_in(message):
        #open Json file and read it
            with open(str(id) + '.json', 'r') as file:
                data = json.load(file)
                #check if the message is a mention
                embeded = discord.Embed(title=f"{data['title']}", description= f"{data['description']}", color=0x00ff00)
                embeded.set_thumbnail(url=f"{data['emote']}")
                await message.reply(embed=embeded)
    await bot.process_commands(message)
bot.run(config.token)

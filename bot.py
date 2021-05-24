import json
import discord
from discord import embeds
from discord.ext import commands
from datetime import datetime, timedelta
import os

import calculation as calc
import function
import track
import mkresult


TOKEN = os.environ['DISCORD_BOT_TOKEN']
ORIGINAL_COLOR = int(os.environ['COLOR'],0)
bot = commands.Bot(command_prefix='%')

MINUTES = 30

@bot.event
async def on_ready():
    print('log in')
    activity = discord.Activity(name=f'%func - {len(bot.guilds)} servers', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.command(aliases=['c','C'])
async def cal(ctx,*args):
    embeds = calc.start(ctx, args)
    for embed in embeds:
        await ctx.send(embed=embed)
@bot.command(aliases=['c6','C6'])
async def cal6(ctx,*args):
    embeds = calc.start(ctx, args, form=6)
    for embed in embeds:
        await ctx.send(embed=embed)
@bot.command(aliases=['c2','C2'])
async def cal2(ctx,*args):
    embeds = calc.start(ctx, args, form=2)
    for embed in embeds:
        await ctx.send(embed=embed)
@bot.command(aliases=['c3','C3'])
async def cal3(ctx,*args):
    embeds = calc.start(ctx, args, form=3)
    for embed in embeds:
        await ctx.send(embed=embed)
@bot.command(aliases=['c4','C4'])
async def cal4(ctx,*args):
    embeds = calc.start(ctx, args, form=4)
    for embed in embeds:
        await ctx.send(embed=embed)

@bot.command(aliases=['s','S'])
async def set(ctx,*args):
    global MINUTES
    message = ctx.message
    channel = message.channel
    messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    sendel = calc.setTeams(ctx, args, messages, author=bot.user)
    if 'embeds' in sendel:
        for embed in sendel['embeds']:
            await channel.send(embed=embed)
    if 'del' in sendel:
        for mg in sendel['del']:
            await mg.delete()

@bot.command(aliases=['o','O'])
async def obs(ctx):
    global MINUTES
    message = ctx.message
    channel = message.channel
    messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    mentions = message.mentions
    sendel = calc.obs(ctx, messages, mentions=mentions, author=bot.user)
    if 'embeds' in sendel:
        for embed in sendel['embeds']:
            await channel.send(embed=embed)
    if 'del' in sendel:
        for mg in sendel['del']:
            await mg.delete()

@bot.command(aliases=['r','R'])
async def result(ctx):
    global MINUTES
    message = ctx.message
    channel = message.channel
    messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    l = calc.result(ctx,messages,author=bot.user)
    if l == None:
        return
    imgDFile, jsonTxt = l
    ch = bot.get_channel(846140589564756068)
    await ch.send(jsonTxt,file=imgDFile)

@bot.command(aliases=['e','E'])
async def edit(ctx,*args):
    pass

@bot.command(aliases=['sd','SD'])
async def send(ctx):
    global MINUTES
    message = ctx.message
    channel = message.channel
    channel_mentions = message.channel_mentions
    if channel_mentions:
        sch = channel_mentions[0]
    else:
        gchs = message.guild.channels
        sch = None
        for gch in gchs:
            if gch.name == '戦績':
                sch = gch
                break
        if sch == None:
            return
    messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    l = calc.send(sch,messages,author=bot.user)
    if l == None:
        return
    imgDFile, jsonTxt = l
    ch = bot.get_channel(846140589564756068)
    await ch.send(jsonTxt,file=imgDFile)

@bot.command(aliases=['f','F'])
async def func(ctx):
    await ctx.send(embed=function.func())

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    global MINUTES
    content = message.content
    channel = message.channel
    sendel = {}

    if message.author.bot:
        if message.author != bot.user:
            return
        if message.embeds:
            embed = message.embeds[0]
            calc.upGSS(embed)
        elif channel == bot.get_channel(846140589564756068):
            jsonData = json.loads(content)
            ch = bot.get_channel(jsonData['id'])
            if jsonData['type'] in['result','send']:
                embed = mkresult.toEmbed(message)
                await ch.send(embed=embed)
        return

    if (calc.is13int(content.replace(' ','').replace('-','')) or content.replace(' ','').replace('-','') == '') and content:
        messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
        sendel = calc.cal(content,messages,author=bot.user)
    
    elif content == 'back':
        messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
        sendel = calc.back(messages,author=bot.user)
    
    elif content == 'func':
        embed = function.old_func()
        await channel.send(embed=embed)
        return
    
    elif content.startswith('calc'):
        if content == 'calc':
            teams = []
        else:
            teams = list(content[5:].split( ))
        embed = function.old_calc(teams)
        await channel.send(embed=embed)
        return
    
    else:
        embed = track.embed(content)
        if not embed == None:
            sendel['embeds'] = [embed]
    
    if 'embeds' in sendel:
        for embed in sendel['embeds']:
            await channel.send(embed=embed)
    if 'del' in sendel:
        for mg in sendel['del']:
            await mg.delete()
    

if __name__ == '__main__':
    bot.run(TOKEN)

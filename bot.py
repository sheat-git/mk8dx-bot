import json
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from datetime import datetime, timedelta
import os

import calculation as calc
import function
import track
import mkresult


TOKEN = os.environ['DISCORD_BOT_TOKEN']
ORIGINAL_COLOR = int(os.environ['COLOR'],0)
BOT_ID = int(os.environ['BOT_ID'])
bot = commands.Bot(command_prefix='%')
slash = SlashCommand(bot, sync_commands=True)

MINUTES = 30


# slash command section

@slash.slash(
    name="cal",
    description='即時集計を始めます',options=[
        create_option(
            name='team1',
            description='チーム名1 (2v2 or 3v3 or 4v4 or 6v6)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team2',
            description='チーム名2 (2v2 or 3v3 or 4v4 or 6v6)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team3',
            description='チーム名3 (2v2 or 3v3 or 4v4)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team4',
            description='チーム名4 (2v2 or 3v3)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team5',
            description='チーム名5 (2v2)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team6',
            description='チーム名6 (2v2)',
            option_type=3,
            required=False
        )
    ])
async def _cal(ctx,team1:str=None,team2:str=None,team3:str=None,team4:str=None,team5:str=None,team6:str=None):
    teams = [team1,team2,team3,team4,team5,team6]
    embeds = calc.start(ctx,teams)
    await ctx.send(embed=embeds[0])
    await ctx.channel.send(embed=embeds[1])

@slash.slash(
    name='set',
    description='チーム名を上書きします',
    options=[
        create_option(
            name='team1',
            description='チーム名1 (2v2 or 3v3 or 4v4 or 6v6)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team2',
            description='チーム名2 (2v2 or 3v3 or 4v4 or 6v6)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team3',
            description='チーム名3 (2v2 or 3v3 or 4v4)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team4',
            description='チーム名4 (2v2 or 3v3)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team5',
            description='チーム名5 (2v2)',
            option_type=3,
            required=False
        ),
        create_option(
            name='team6',
            description='チーム名6 (2v2)',
            option_type=3,
            required=False
        )
    ])
async def _set(ctx,team1:str=None,team2:str=None,team3:str=None,team4:str=None,team5:str=None,team6:str=None):
    teams = [team1,team2,team3,team4,team5,team6]
    messages = await ctx.channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    sed = calc._setTeams(ctx,messages,teams)
    if 'send' in sed:
        for sendict in sed['send']:
            await ctx.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'),hidden=True)
    if 'edit' in sed:
        for edict in sed['edit']:
            await edict['message'].edit(content=edict.get('content'),embed=edict.get('embed'),file=edict.get('file'))

@slash.slash(
    name='obs',
    description='配信用に即時集計レイヤーのURLを発行し、更新を始めます')
async def _obs(ctx):
    messages = await ctx.channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    sed = calc._obs(ctx,messages)
    if 'send' in sed:
        for sendict in sed['send']:
            await ctx.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'),hidden=True)
    if 'edit' in sed:
        for edict in sed['edit']:
            await edict['message'].edit(content=edict.get('content'),embed=edict.get('embed'),file=edict.get('file'))

@slash.slash(name='result',description='即時に基づいた集計表を作成します')
async def _result(ctx):
    messages = await ctx.channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    sed = calc.result(messages)
    if not sed:
        await ctx.send(content='ERROR: 過去30分以内/100件以内に即時集計がみつからない or 形式が6v6でない or 12レース完走していない')
    if 'send' in sed:
        for sendict in sed['send']:
            await ctx.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'))

@slash.slash(name='send',description='集計表を作成し「戦績」チャンネルに送ります',options=[create_option(name='channel',description='「戦績」ではなく指定したチャンネルに送ります',option_type=7,required=False)])
async def _send(ctx,channel=None):
    if channel == None:
        gchs = ctx.guild.channels
        for gch in gchs:
            if gch.name == '戦績':
                channel = gch
                break
        if channel == None:
            await ctx.send(content='ERROR: 「戦績」チャンネルがない or 権限がない')
            return
    messages = await ctx.channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    sed = calc.result(messages,cmd='send')
    if not sed:
        await ctx.send(content='ERROR: 過去30分以内/100件以内に即時集計がみつからない or 形式が6v6でない or 12レース完走していない')
    if 'send' in sed:
        for sendict in sed['send']:
            await channel.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'))
            await ctx.send(content='送信しました')

@slash.slash(
    name="cal2",
    description='2v2の即時集計を始めます', 
    options=[
        create_option(
            name='team1',
            description='チーム名1',
            option_type=3,
            required=False
        ),
        create_option(
            name='team2',
            description='チーム名2',
            option_type=3,
            required=False
        ),
        create_option(
            name='team3',
            description='チーム名3',
            option_type=3,
            required=False
        ),
        create_option(
            name='team4',
            description='チーム名4',
            option_type=3,
            required=False
        ),
        create_option(
            name='team5',
            description='チーム名5',
            option_type=3,
            required=False
        ),
        create_option(
            name='team6',
            description='チーム名6',
            option_type=3,
            required=False
        )
    ])
async def _cal2(ctx,team1:str=None,team2:str=None,team3:str=None,team4:str=None,team5:str=None,team6:str=None):
    teams = [team1,team2,team3,team4,team5,team6]
    embeds = calc.start(ctx, teams, form=2)
    await ctx.send(embed=embeds[0])
    await ctx.channel.send(embed=embeds[1])
@slash.slash(
    name="cal3",
    description='3v3の即時集計を始めます', 
    options=[
        create_option(
            name='team1',
            description='チーム名1',
            option_type=3,
            required=False
        ),
        create_option(
            name='team2',
            description='チーム名2',
            option_type=3,
            required=False
        ),
        create_option(
            name='team3',
            description='チーム名3',
            option_type=3,
            required=False
        ),
        create_option(
            name='team4',
            description='チーム名4',
            option_type=3,
            required=False
        )
    ])
async def _cal3(ctx,team1:str=None,team2:str=None,team3:str=None,team4:str=None):
    teams = [team1,team2,team3,team4]
    embeds = calc.start(ctx, teams, form=3)
    await ctx.send(embed=embeds[0])
    await ctx.channel.send(embed=embeds[1])
@slash.slash(
    name="cal4",
    description='4v4の即時集計を始めます', 
    options=[
        create_option(
            name='team1',
            description='チーム名1',
            option_type=3,
            required=False
        ),
        create_option(
            name='team2',
            description='チーム名2',
            option_type=3,
            required=False
        ),
        create_option(
            name='team3',
            description='チーム名3',
            option_type=3,
            required=False
        )
    ])
async def _cal4(ctx,team1:str=None,team2:str=None,team3:str=None):
    teams = [team1,team2,team3]
    embeds = calc.start(ctx, teams, form=4)
    await ctx.send(embed=embeds[0])
    await ctx.channel.send(embed=embeds[1])
@slash.slash(
    name="cal6",
    description='6v6の即時集計を始めます', 
    options=[
        create_option(
            name='team1',
            description='チーム名1',
            option_type=3,
            required=False
        ),
        create_option(
            name='team2',
            description='チーム名2',
            option_type=3,
            required=False
        )
    ])
async def _cal6(ctx,team1:str=None,team2:str=None):
    teams = [team1,team2]
    embeds = calc.start(ctx, teams, form=6)
    await ctx.send(embed=embeds[0])
    await ctx.channel.send(embed=embeds[1])



# normal bot section

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
    messages = await ctx.message.channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    sed = calc.setTeams(ctx,messages,args)
    if 'send' in sed:
        for sendict in sed['send']:
            await ctx.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'))
    if 'edit' in sed:
        for edict in sed['edit']:
            await edict['message'].edit(content=edict.get('content'),embed=edict.get('embed'),file=edict.get('file'))
    if 'del' in sed:
        for mg in sed['del']:
            await mg.delete()

@bot.command(aliases=['o','O'])
async def obs(ctx):
    messages = await ctx.message.channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    mentions = ctx.message.mentions
    sed = calc.obs(ctx, messages, mentions=mentions)
    if 'send' in sed:
        for sendict in sed['send']:
            await ctx.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'))
    if 'edit' in sed:
        for edict in sed['edit']:
            await edict['message'].edit(content=edict.get('content'),embed=edict.get('embed'),file=edict.get('file'))
    if 'del' in sed:
        for mg in sed['del']:
            await mg.delete()

@bot.command(aliases=['r','R'])
async def result(ctx):
    messages = await ctx.message.channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    sed = calc.result(messages)
    if 'send' in sed:
        for sendict in sed['send']:
            await ctx.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'))

@bot.command(aliases=['sd','SD'])
async def send(ctx):
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
    sed = calc.result(messages,cmd='send')
    if 'send' in sed:
        for sendict in sed['send']:
            await sch.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'))

@bot.command(aliases=['editT','eT','t','T'])
async def editTrack(ctx,*args):
    messages = await ctx.message.channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
    sed = calc.editTrack(ctx,messages,args)
    if 'send' in sed:
        for sendict in sed['send']:
            await ctx.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'))
    if 'edit' in sed:
        for edict in sed['edit']:
            await edict['message'].edit(content=edict.get('content'),embed=edict.get('embed'),file=edict.get('file'))
    if 'del' in sed:
        for mg in sed['del']:
            await mg.delete()

@bot.command(aliases=['f','F'])
async def func(ctx):
    await ctx.send(embed=function.func())

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    content = message.content
    channel = message.channel
    sed = {}

    if message.author.bot:
        if message.author != bot.user:
            return
        if message.embeds:
            embed = message.embeds[0]
            calc.upGSS(embed)
        elif channel == bot.get_channel(846140589564756068):
            jsonData = json.loads(content)
            return
        return

    if (calc.is10int(content.replace(' ','').replace('-','')) or content.replace(' ','').replace('-','') == '') and content:
        messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
        sed = calc.cal(content,messages)
    
    elif content == 'back':
        messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = MINUTES), oldest_first=False).flatten()
        sed = calc.back(messages)
    
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
            sed['send'] = [{'embed':embed}]
    
    if 'send' in sed:
        for sendict in sed['send']:
            await channel.send(content=sendict.get('content'),embed=sendict.get('embed'),file=sendict.get('file'))
    if 'edit' in sed:
        for edict in sed['edit']:
            await edict['message'].edit(content=edict.get('content'),embed=edict.get('embed'),file=edict.get('file'))
    if 'del' in sed:
        for mg in sed['del']:
            await mg.delete()


@bot.event
async def on_raw_message_edit(payload):
    author_id = int(payload.data['author']['id'])
    if author_id == BOT_ID:
        embeds = payload.data['embeds']
        if embeds:
            embed_dict = embeds[0]
            calc.upGSS(embed=None,embed_dict=embed_dict)


bot.run(TOKEN)

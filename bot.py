import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import calc
import track


auther_name = os.environ['name']
auther_num = os.environ['num']
TOKEN = os.environ['DISCORD_BOT_TOKEN']

client = commands.Bot(command_prefix='!sheat ')


@client.event
async def on_ready():
    print('ログインしました')
    activity = discord.Activity(name=f'"func"で機能説明 - {len(client.guilds)} servers', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    content = message.content
    channel = message.channel

    # calc
    if content == 'calc':
        main_match_dict = {'match_type':6, 'enemy_list':[], 'sum_score_list':[0,0], 'race_list':[], 'run_track_dict':{}}
        await channel.send(embed = discord.Embed.from_dict(calc.to_main_embed_dict(main_match_dict)))
    elif content.startswith('calc') and ' ' in content:
        enemy_list = list(content.split(' '))[1:]
        if not len(enemy_list) in [1,2,3,5]:
            await channel.send('チーム数おかしいかも:cry:')
        else:
            main_match_dict = {'match_type':12//(len(enemy_list)+1), 'enemy_list':enemy_list, 'sum_score_list':[0]*(len(enemy_list)+1), 'race_list':[], 'run_track_dict':{}}
            await channel.send(embed = discord.Embed.from_dict(calc.to_main_embed_dict(main_match_dict)))
    elif str.isdecimal(content.replace(' ','')) or content in ['back', 'now']:
        main_match_message = None
        sub_match_message = None
        run_track = None
        messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = 20)).flatten()
        for m in reversed(messages):
            if m.author.name == auther_name and m.author.discriminator == auther_num and len(m.embeds) != 0:
                embed_dict = m.embeds[0].to_dict()
                if 'image' in embed_dict and embed_dict['image']['url'].startswith('https://raw.githubusercontent.com/sheat-git/mk8dx/main/files/') and run_track == None:
                    run_track = embed_dict['title']
                elif embed_dict['title'].startswith('race') and sub_match_message == None:
                    sub_match_message = m
                    sub_match_dict = calc.to_sub_match_dict(embed_dict)
                elif embed_dict['title'].startswith('即時集計'):
                    main_match_message = m
                    main_match_dict = calc.to_main_match_dict(embed_dict)
                    break
        if main_match_message == None:
            pass
        elif content == 'back':
            if sub_match_message == None:
                await channel.send(embed = discord.Embed.from_dict(calc.to_main_embed_dict(calc.back(main_match_dict))))
                await main_match_message.delete()
            else:
                sub_match_message.delete()
        elif content == 'now':
            await channel.send(embed = discord.Embed.from_dict(calc.create_status(main_match_dict)))
        elif len(main_match_dict['race_list']) >= 12:
            pass
        else:
            if sub_match_message == None:
                rank_lists = []
                race = len(main_match_dict['race_list']) + 1
            else:
                rank_lists = sub_match_dict['rank_lists']
                race = sub_match_dict['race']
                if not sub_match_dict['run_track'] == None:
                    run_track = sub_match_dict['run_track']
            match_type = main_match_dict['match_type']
            rank_lists = calc.create_rank_lists(match_type, content, rank_lists)
            if rank_lists == None:
                return
            if match_type != 6:
                sub_match_dict = calc.create_sub_match_dict(match_type, main_match_dict['enemy_list'], race, rank_lists, run_track)
                await channel.send(embed = discord.Embed.from_dict(calc.to_sub_embed_dict(sub_match_dict)))
                if not sub_match_message == None:
                    await sub_match_message.delete()
            if len(rank_lists) == 12 // match_type:
                await channel.send(embed = discord.Embed.from_dict(calc.calculation(main_match_dict, rank_lists, run_track)))
                await main_match_message.delete()
    else:
        # track
        send_track_list = track.search(content)
        if not send_track_list == None:
            track_embed = discord.Embed(title = send_track_list[0].replace(':',' '))
            track_embed.set_image(url = send_track_list[1])
            await channel.send(embed = track_embed)
        send_tracks_list = track.type_search(content)
        if not send_tracks_list == None:
            description = ''
            for i in send_tracks_list[1]:
                description += track.search(i)[0].replace(':', ' ') + '\n'
            tracks_embed = discord.Embed(title = send_tracks_list[0], description = description[:-1])
            await channel.send(embed = tracks_embed)
        
        # function
        if content in ['func', '"func"', "''func''", 'FUNC', '"FUNC"', "''FUNC''"]:
            func_embed = discord.Embed(title = '機能説明')
            func_embed.set_author(name="twitter:@sheat_MK", url="https://twitter.com/sheat_MK", icon_url="https://pbs.twimg.com/profile_images/1315419578646708224/DqNBLGeY_400x400.jpg")
            func_embed.add_field(name = 'コース名  (例:`ベビぱ`)', value = 'コース名の略称から英語名・日本語名をフルで返答します\n全てのコース名に反応するのでチャンネルに応じてこのbotの「メッセージを読む」権限を剥奪してください\n** **', inline=False)
            func_embed.add_field(name = '即時集計  (例:`calc BP`)', value = 'calc で始めることができます\n`calc` : 6v6\n`calc tag1` : tag1との6v6\n`calc tag1 tag2` : tag1,tag2との4v4\n`calc tag1 tag2 tag3`\n : tag1,tag2,tag3との3v3\n`calc tag1 tag2 tag3 tag4 tag5`\n : tag1-tag5との2v2\n点数入力は2通りできます\n**1.チームごとに空白区切り**\n\t`123 456 789`\n\t上記のようにしてあなたのチーム,tag1,tag2の順に入力します\n\t最後のチームの点数は補完されます\n**2.チームごとに送信**\n\t`123`\n\t`456`\n\t`789`\n\t上記のように順に送信してください\n\t1と同様に最後のチームは補完されます\n** **', inline=False)
            func_embed.add_field(name = '即時集計のコース記録', value = '前回の即時の入力から次回集計までに入力されたコースのうち、最新のものを記録していきます', inline=False)
            await channel.send(embed = func_embed)


if __name__ == '__main__':
    client.run(TOKEN)

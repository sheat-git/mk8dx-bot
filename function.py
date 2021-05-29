import discord
import os

from matplotlib.pyplot import title


ORIGINAL_COLOR = int(os.environ['COLOR'],0)

MINUTES = 30

def calStartEmbed(teams,form=0,caln=0,args=()):
    newLine = '\n'
    if not form:
        form = 12//len(teams)
    embed_dict = {}
    embed_dict['title'] = f'即時集計 {form}v{form} START!'
    embed_dict['description'] = f'{MINUTES}分間何も操作しないと更新ができなくなります。'
    fields = []
    if not caln and len(args) in [2,3]:
        mayForm = 12//(len(args)+1)
        fields.append({'name':f'__{mayForm}v{mayForm}の即時がしたい__','value':f'```fix{newLine}%cal{mayForm} {" ".join(args)} または %cal{mayForm} YourTeam {" ".join(args)}```','inline':False})
    sampleTeams = ['RR','SS','TT','XX','YY','ZZ'][:12//form]
    fields.append({'name':'__チーム名を変更したい__','value':f'```fix{newLine}%set {" ".join(sampleTeams)}```-> チーム名が{",".join(sampleTeams)}に','inline':False})
    fields.append({'name':'__配信用に即時集計レイヤーのURLを発行したい__','value':'```fix\n%obs```※urlは発行したユーザー毎に固定です。\n__即時集計毎に__コマンドを実行してください。','inline':False})
    fields.append({'name':'__集計表を作成したい__','value':'```fix\n%result```即時集計より集計表を作成します。12レース完走後に使用可能です。','inline':False})
    embed_dict['fields'] = fields
    embed_dict['color'] = ORIGINAL_COLOR
    return discord.Embed.from_dict(embed_dict)

def calObsEmbed(users):
    embed_dict = {}
    embed_dict['title'] = f'即時集計レイヤー URL'
    embed_dict['description'] = 'どのサーバーでもユーザー毎のURLは変わりません！\n※Discordのユーザー名を変更するとURLも変わってしまいます...（ニックネームは関係なし）'
    url = 'https://sheat-git.github.io/sokuji/?user='
    fields = []
    for user in users:
        field = {'name':f'{user[:-4]} さん用 更新開始','value':url+user}
        fields.append(field)
    embed_dict['fields'] = fields
    embed_dict['footer'] = {'text':'Copyright (c) 2020 GungeeSpla'}
    embed_dict['color'] = ORIGINAL_COLOR
    return discord.Embed.from_dict(embed_dict)

def func():
    embed_dict = {}
    embed_dict['author'] = {'name':"twitter:@sheat_MK", 'url':"https://twitter.com/sheat_MK", 'icon_url':"https://pbs.twimg.com/profile_images/1315419578646708224/DqNBLGeY_400x400.jpg"}
    embed_dict['title'] = 'コマンド一覧'
    embed_dict['description'] = \
        '`%cal AA BB...` : 即時集計開始.デフォルトでは6v6.入力されたチーム数に応じて形式を判別\n' + \
        '`%cal6 AA` : AAとの6v6即時集計開始.自身のチーム名も含め `%cal6 ZZ AA` としても良い\n' + \
        '`%cal2 AA BB...` : AA,BB,...との2v2即時集計開始.自身のチーム名も含め `%cal2 ZZ AA BB...` としても良い\n' + \
        '`%cal3 AA BB CC` : AA,BB,CCとの3v3即時集計開始.自身のチーム名も含め `%cal3 ZZ AA BB CC` としても良い\n' + \
        '`%cal4 AA BB` : AA,BBとの4v4即時集計開始.自身のチーム名も含め `%cal4 ZZ AA BB` としても良い\n' + \
        '> 上記`%cal`系コマンドはチーム名を入力しなくても使用可.ただしチーム名は自動で決まる\n' + \
        '`%set RR SS...` : チーム名を変更.全チーム名を入力 (一部のみ変更は不可)\n' + \
        '`%obs` : 即時集計開始後に使える.配信用に即時集計レイヤーのURLを発行\n' + \
        '`%result` : 6v6のみ即時集計終了後に使える.即時に基づいた集計表を作成\n' + \
        '`%send` : 集計表を作成し「戦績」チャンネルに送る'
    fields = []
    value = \
        '**コース名** (常時反応)\n' + \
        '> コース名の略称に対して、英語名略称•日本語名フルを画像つきで送る\n' + \
        '**コース名記録** (即時中のみ)\n' + \
        '> 次回の順位入力までに送信されたコースのうち最新のコース名を即時集計に反映\n' + \
        '**順位入力** (即時中のみ)\n' + \
        '> 順位を前から連続で打てば良い\n' + \
        '> 6v6以外ではチーム毎に順位を送信.また空白区切りでまとめて送信も可\n' + \
        '> 例 : `2,3,4,5,10,11` 位のとき\n' + \
        '> `23451011` と入力.または `2-51011` と省略できる\n' + \
        '> 前6,下6の `1-6`, `7-12` 等はさらに省略し `-6`, `7-` も可能\n' + \
        '**順位修正** (即時中のみ)\n' + \
        '> `back` で一つ前の状態に戻れる'
    fields.append({'name':'コマンド外操作','value':value,'inline':False})
    embed_dict['fields'] = fields
    embed_dict['color'] = ORIGINAL_COLOR
    return discord.Embed.from_dict(embed_dict)

def old_calc(teams):
    if teams:
        if len(teams) > 6:
            teams = teams[:6]
        len3formDict = {1:6,2:4,3:3,4:3,5:2,6:2}
        cmd = f'%cal{len3formDict[len(teams)]} ' + ' '.join(teams)
    else:
        cmd = r'%cal'
    newLine = '\n'
    embed_dict = {}
    embed_dict['title'] = 'botが生まれ変わりました！'
    embed_dict['description'] = \
        f'```fix{newLine}{cmd}```上記コマンドに変更になりました。' + \
        f'```fix{newLine}%func```詳しくは上記コマンドで'
    embed_dict['color'] = ORIGINAL_COLOR
    return discord.Embed.from_dict(embed_dict)

def old_func():
    embed_dict = {}
    embed_dict['title'] = 'botが生まれ変わりました！'
    embed_dict['description'] = \
        '```fix\n%func```上記コマンドに変更になりました。'
    embed_dict['color'] = ORIGINAL_COLOR
    return discord.Embed.from_dict(embed_dict)

def nonCalcEmbed():
    return discord.Embed(title='有効な即時集計が見つかりません',description='先に即時集計を始めてください\n始めていても30分間何も操作がないは更新できません',color=ORIGINAL_COLOR)

def existObsEmbed():
    return discord.Embed(title='すでにURLは発行・更新されています',description='即時集計の最下部の"OBS更新 for"にあなたの名前があれば更新が続いています',color=ORIGINAL_COLOR)

def successEmbed():
    return discord.Embed(title='成功しました！',color=ORIGINAL_COLOR)

def changeEmbed():
    return discord.Embed(title='変更しました',color=ORIGINAL_COLOR)

def sendEmbed():
    return discord.Embed(title='送信しました',color=ORIGINAL_COLOR)

def nonSensekiEmbed():
    return discord.Embed(title='「戦績」チャンネルがありません',description='権限がない可能性もあります',color=ORIGINAL_COLOR)
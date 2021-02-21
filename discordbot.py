import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os

# herokuからtokunを取得
TOKEN = os.environ['DISCORD_BOT_TOKEN']

# client = discord.Client()
client = commands.Bot(command_prefix='!sheat ')

def search_track(name):
    DKJ_list = ['DKJ', 'dkj', 'じゃんぐる', 'ジャングル', 'jk', 'JK']
    PPS_list = ['PPS', 'pps', 'パクスラ', 'パックンスライダー', 'ぱくすら', 'ぱっくんすらいだー', 'パックン', 'ぱっくん']
    MP_list = ['MP', 'mp', 'ミュージックパーク', 'ミューパ', 'ミューぱ', 'みゅーじっくぱーく', 'みゅーぱ']
    TTC_list = ['TTC', 'ttc', 'チクタクロック', 'チクタク', 'ティックトック', 'チックタック', 'ちっくたっく', 'ちくたくろっく', 'ちくたく', 'てぃっくとっく']
    CCB_list = ['CCB', 'ccb', 'プクプクビーチ', 'プクプク', 'プクビ', 'ぷくぷくびーち', 'ぷくぷく', 'ぷくび', 'びーち', 'ビーチ']
    WS_list = ['WS', 'ws', 'ワリオスタジアム', 'ワリスタ', 'わりすた', 'わりおすたじあむ']
    rMC_list = ['rMC', 'rmc', 'RMC', 'GBA', 'ぐば', 'グバ', 'GBAまりさ', 'GBAマリサ', 'GBAマリオサーキット', 'GBAまりおさーきっと', 'ジービーエー', 'ジビエ', 'じーびーえー', 'じびえ', 'gba']
    rDDD_list = ['rDDD', 'rddd', 'RDDD', 'カラカラ', 'カラサバ', 'からさば', 'からから', 'カラカラ砂漠', 'からからさばく', 'カラカラさばく', 'カラカラサバク']
    SL_list = ['SL', 'sl', 'しゃべらん', 'シャベラン', 'シャーベットランド', 'しゃーべっとらんど', 'シャーベット', 'しゃーべっと']
    dYC_list = ['dYC', 'dyc', 'DYC', 'ヨシサ', 'ヨッシーサーキット', 'よしさ', 'よっしーさーきっと']
    TT_list = ['TT', 'tt', 'キノピオハイウェイ', '高速道路', '高速', 'こうそくどうろ', 'こうそく', 'はいうぇい', 'ハイウェイ', 'きのぴおはいうぇい']
    rRRy_list = ['rRRy', 'rrry', 'RRRY', 'ピーチサーキット', 'ぴーちさーきっと', 'ピチさ', 'ピチサ', 'ぴちさ']
    YV_list = ['YV', 'yv', 'ヨシバ', 'よっしーバレー', 'よっしーばれー', 'ヨッシーバレー', 'よしば', 'バレー', 'ばれー']
    rRRd_list = ['rRRd', 'rrrd', 'RRRD', '64虹', '６４虹', '64にじ', '６４にじ', 'ろくよん', 'ロクヨン']
    DP3_list = ['DP3', 'dp3', 'ドーナツへいや', 'どーなつへいや', 'ドーナツ平野', 'どーなつ平野', 'ドーナツヘイヤ', '平野', 'へいや']
    dRR_list = ['dRR', 'drr', 'DRR', 'SFC', 'sfc', 'SFCにじ', 'SFC虹', 'sfcにじ', 'sfc虹', 'えすえふしー', 'エスエフシー', 'SFCレインボーロード', 'sfcレインボーロード', 'SFCれいんぼーろーど', 'sfcれいんぼーろーど', 'えすえふしーにじ', 'エスエフシーニジ']
    GV_list = ['GV', 'gv', 'ぐらぐら', 'グラグラ', 'グラグラ火山', 'ぐらぐら火山', 'グラグラカザン', 'ぐらぐらかざん', '火山', 'かざん']
    MMM_list = ['MMM', 'mmm', 'モモカン', 'もーもーカントリー', 'モーモーカントリー', 'ももかん', 'もーもーかんとりー', '牛', 'うし']
    dWGM_list = ['dWGM', 'dwgm', 'DWGM', 'ワリオこうざん', 'ワリオ鉱山', 'わりおこうざん', 'わりこう', 'ワリこう', 'ワリ鉱', 'わり鉱']
    WP_list = ['WP', 'wp', 'ウォーターパーク', 'ヲーターパーク', 'うぉーたーぱーく', 'をーたーぱーく', 'をたぱ', 'ヲタパ', 'うぉたぱ', 'ウォタパ', '水公園', 'オタぱ', 'おたぱ', 'オタパ']
    dEA_list = ['dEA', 'dea', 'DEA', 'エキサイトバイク', '役馬', 'エキバ', 'えきば', 'えきさいとばいく']
    Ed_list = ['Ed', 'ed', 'ED', 'エレドリ', 'エレド', 'エレクトロドリーム', 'えれどり', 'えれど', 'えれくとろどりーむ', '夢']
    TH_list = ['TH', 'th', 'キノピオハーバー', 'きのぴおはーばー', 'はーばー', 'ハーバー']
    BC_list = ['BC', 'bc', 'クッパキャッスル', 'くっぱきゃっする', 'くっきゃぱっする', 'クッキャパッスル', 'くぱきゃ', 'クパキャ']
    SA_list = ['SA', 'sa', 'サンシャイン空港', 'サンシャインくうこう', 'さんしゃいんくうこう', '空港', 'くうこう']
    SSC_list = ['SSC', 'ssc', 'スイーツキャニオン', 'すいーつきゃにおん', 'スイキャニ', 'すいきゃに']
    CC_list = ['CC', 'cc', 'スカイガーデン', 'スカが', 'すかが', 'スカガ', 'すかいがーでん']
    dIIO_list = ['dIIO', 'diio', 'DIIO', 'ツルツルツイスター', 'つるつるついすたー', 'ツツツ', 'つつつ', 'ツイスター', 'ついすたー', 'ツルツル', 'つるつる']
    TR_list = ['TR', 'tr', 'ドッスン遺跡', 'どっすんいせき', 'ドッスンいせき', 'ドッスン', 'どっすん', 'いせき', '遺跡', 'イセキ', 'ドッスンイセキ']
    dDD_list = ['dDD', 'ddd', 'DDD', 'ドラロ', 'どらろ', 'ドラゴンロード', 'どらごんろーど']
    DS_list = ['DS', 'ds', 'ドルフィンみさき', 'ドルフィン岬', 'どるふぃんみさき', 'どるふぃん岬', 'どるみ', 'ドルミ', 'どるふぃん', 'ドルフィン']
    TM_list = ['TM', 'tm', 'ねじれマンション', 'ねじれまんしょん', 'ねじまん', 'ねじマン', 'ネジマン', 'まんしょん', 'マンション', 'ねじれ', 'ネジレ', 'ネジション', 'ねじしょん', 'ねじション', 'ネジしょん', 'ねじねじ', 'ネジネジ', 'ねじ', 'ネジ']
    dHC_list = ['dHC', 'dhc', 'DHC', 'ハイラルサーキット', 'はいらる', 'はいらるさーきっと', 'ハイラル', 'は', 'ハ']
    SFG_list = ['SFG', 'sfg', 'へいほーこうざん', 'ヘイホー鉱山', 'ヘイホーこうざん', 'へいほー鉱山', 'へいこう', 'ヘイコウ', 'へい鉱', 'ヘイ鉱', 'ヘイこう']
    BDD_list = ['BDD', 'bdd', 'ホネホネさばく', 'ホネホネ砂漠', 'ほねほねさばく', 'ほねほね砂漠', '骨骨砂漠', '骨骨さばく', 'ホネホネサバク', 'ほねさば', '骨サバ', 'ホネサバ', '骨', 'ほね', 'ホネ', 'ほねほね', '骨骨', 'ホネホネ']
    MKS_list = ['MKS', 'mks', 'マリオカートスタジアム', 'まりおかーとすたじあむ', 'マリカす', 'マリカス', 'まりかす']
    MC_list = ['MC', 'mc', 'マリオサーキット', 'マリサ', 'まりおさーきっと', 'まりさ', '新マリサ', 'しんまりさ', 'シンマリサ', '新まりさ']
    RR_list = ['RR', 'rr', '新虹', 'しんにじ', 'レインボーロード', 'シンニジ', 'れいんぼーろーど']
    dMC_list = ['dMC', 'dmc', 'DMC', 'ミュートシティ', 'ミュート', 'みゅーと', 'みゅーとしてぃ']
    dBP_list = ['dBP', 'dbp', 'DBP', 'BP', 'bp', 'ベビィパーク', 'ベビーパーク', 'べびぃぱーく', 'べびーぱーく', 'べびぱ', 'ベビパ']
    dCL_list = ['dCL', 'dcl', 'DCL', 'チーズランド', 'ちーずらんど', 'ちーず', 'チーズ']
    dWW_list = ['dWW', 'dww', 'DWW', 'ネイチャーロード', 'ねいちゃーろーど', 'ネイチャー', 'ねいちゃー', 'なちゅれ', 'ナチュレ']
    dAC_list = ['dAC', 'dac', 'DAC', 'ac', 'AC', 'どうぶつの森', 'どうもり', '動物の森', 'どう森', 'ぶつ森', 'ぶつもり', 'ドウブツノモリ', 'ドウモリ', 'ブツモリ']
    dNBC_list = ['dNBC', 'dnbc', 'DNBC', 'ネオクッパシティ', 'ねおくっぱしてぃ', 'ネオぱ', 'ネオパ', 'ねおぱ', 'ねおくっぱ', 'ネオクッパ']
    dRiR_list = ['dRiR', 'DRIR', 'drir', 'リボンロード', 'リボン', 'りぼんろーど', 'りぼん']
    dSBS_list = ['dSBS', 'dsbs', 'DSBS', 'リンリンメトロ', 'りんりんめとろ', 'りんめと', 'リンメト', 'リンリン', 'りんりん', 'リン', 'りん', '凛']
    BB_list = ['BB', 'bb', 'ビッグブルー', 'びっぐぶるー']
    MW_list = ['MW', 'mw', 'ワリオスノーマウンテン', 'わりおすのーまうんてん', 'ワリスノ', 'わりすの', '雪山', 'ゆきやまうんてん', 'すの', 'スノ']
    tracks_list = [ \
        [['MKS:マリオカートスタジアム', MKS_list], ['WP:ウォーターパーク', WP_list], ['SSC:スイーツキャニオン', SSC_list], ['TR:ドッスンいせき', TR_list]], \
        [['MC:新マリオサーキット', MC_list], ['TH:キノピオハーバー', TH_list], ['TM:ねじれマンション', TM_list], ['SFG:ヘイホーこうざん', SFG_list]], \
        [['SA:サンシャインくうこう', SA_list], ['DS:ドルフィンみさき', DS_list], ['Ed:エレクトロドリーム', Ed_list], ['MW:ワリオスノーマウンテン', MW_list]], \
        [['CC:スカイガーデン', CC_list], ['BDD:ホネホネさばく', BDD_list], ['BC:クッパキャッスル', BC_list], ['RR:新レインボーロード', RR_list]], \
        [['dYC:ヨッシーサーキット', dYC_list], ['dEA:エキサイトバイク', dEA_list], ['dDD:ドラゴンロード', dDD_list], ['dMC:ミュートシティ', dMC_list]], \
        [['dBP:ベビィパーク', dBP_list], ['dCL:チーズランド', dCL_list], ['dWW:ネイチャーロード', dWW_list], ['dAC:どうぶつの森', dAC_list]], \
        [['MMM:モーモーカントリー', MMM_list], ['rMC:GBAマリオサーキット', rMC_list], ['CCB:プクプクビーチ', CCB_list], ['TT:キノピオハイウェイ', TT_list]], \
        [['rDDD:カラカラさばく', rDDD_list], ['DP3:ドーナツへいや', DP3_list], ['rRRy:ピーチサーキット', rRRy_list], ['DKJ:DKジャングル', DKJ_list]], \
        [['WS:ワリオスタジアム', WS_list], ['SL:シャーベットランド', SL_list], ['MP:ミュージックパーク', MP_list], ['YV:ヨッシーバレー', YV_list]], \
        [['TTC:チクタクロック', TTC_list], ['PPS:パックンスライダー', PPS_list], ['GV:グラグラかざん', GV_list], ['rRRd:64レインボーロード', rRRd_list]], \
        [['dWGM:ワリオこうざん', dWGM_list], ['dRR:SFCレインボーロード', dRR_list], ['dIIO:ツルツルツイスター', dIIO_list], ['dHC:ハイラルサーキット', dHC_list]], \
        [['dNBC:ネオクッパシティ', dNBC_list], ['dRiR:リボンロード', dRiR_list], ['dSBS:リンリンメトロ', dSBS_list], ['BB:ビッグブルー', BB_list]]]
    for i in range(12):
        for j in range(4):
            if name in tracks_list[i][j][1]:
                return [tracks_list[i][j][0], f'https://raw.githubusercontent.com/sheat-git/mk8dx/main/files/{i+1}.JPG']


def search_tracks(mc):
    front = ['前コース', '前コ', '前こ', '前', '前個', 'まえこ', 'まえ', 'まえこーす']
    mid = ['中位コース', '中位コ', '中位こ', '中位', '中', 'なか', 'ちゅうい', 'ちゅういこ', 'ちゅういこーす']
    back = ['打開コース', '打開コ', '打開こ', 'だかいこ', '打開', 'だかいこーす', 'だかい', 'うしろ', '後', '後ろ']
    strategy_dict = {'前コース':['WS', 'dNBC', 'DKJ', 'dHC', 'MW', 'TTC'], '中位コース':['TM', 'Ed', 'DS', 'dIIO', 'MP', 'MMM'], '打開コース':['dCL', 'rDDD', 'dEA', 'YV', 'rMC', 'DP3']}
    for i in [front, mid, back]:
        if mc in i:
            return [i[0],strategy_dict[i[0]]]

def count_limit_check(replies_count, mkmg_type, mkmgall):
    if mkmgall == 1:
        return True
    elif replies_count < 12 // mkmg_type - 1:
        return True
    else:
        return False

def calc_score(match_type, rank_lists):
    to_score = {1:15,2:12,3:10,4:9,5:8,6:7,7:6,8:5,9:4,10:3,11:2,12:1,0:0}
    score_list = [0] * (12//match_type)
    for i in range(len(rank_lists)):
        rank_list = list(rank_lists[i])
        if match_type + 1 <= len(rank_list) <= match_type + 3:
            rank_list[-2] += rank_list[-1]
            del rank_list[-1]
        if match_type + 1 <= len(rank_list) <= match_type + 2:
            rank_list[-3] += rank_list[-2]
            del rank_list[-2]
        if len(rank_list) == match_type + 1:
            rank_list[-4] += rank_list[-3]
            del rank_list[-3]
        for j in rank_list:
            score_list[i] += to_score[int(j)]
        if i == 0:
            rank_list_1 = rank_list
    if score_list[-1] == 0:
        all_score = True
        for score in score_list:
            if score == 0:
                all_score == False
        if all_score:
            score_list[-1] = 82
            for score in score_list[:-1]:
                score_list[-1] -= score
    return [rank_list_1, score_list]

def calc_sum_score(des_text, score_list):
    sum_score_list = list(map(int, des_text.split(' : ')))
    for i in range(len(sum_score_list)):
        sum_score_list[i] += score_list[i]
    return sum_score_list

def create_calc_embed(match_type, mc, calc_dict, run_track):
    rs_list = calc_score(match_type, list(mc.split(' ')))
    rank_list = rs_list[0]
    score_list = rs_list[1]
    sum_score_list = calc_sum_score(' : '.join(list(map(lambda x: str(x.split(' (')[0]), calc_dict['description'].split(' @')[0].split(' : ')))), score_list)
    value_score = ''
    for score in score_list:
        if value_score == '':
            value_score = str(score)
        else:
            dif = score_list[0] - score
            if dif > 0:
                value_score += f' : {score} (+{dif})'
            else:
                value_score += f' : {score} ({dif})'
    value_rank = ''
    for rank in rank_list:
        value_rank += f',{rank}'
    value = value_score + ' | ' + value_rank[1:]
    description_score = ''
    for sum_score in sum_score_list:
        if description_score == '':
            description_score = str(sum_score)
        else:
            dif = sum_score_list[0] - sum_score
            if dif > 0:
                description_score += f' : {sum_score} (+{dif})'
            else:
                description_score += f' : {sum_score} ({dif})'
    if not 'fields' in calc_dict:
        calc_embed = discord.Embed(title = calc_dict['title'], description = description_score + f' @{int(calc_dict["description"].split(" @")[1]) - 1}', color = 0xd2cab6)
        calc_embed.add_field(name = 'race1 ' + run_track, value = value, inline = False)
    else:
        calc_embed = discord.Embed(title = calc_dict['title'], description = description_score + f' @{int(calc_dict["description"].split(" @")[1]) - 1}', color = 0xd2cab6)
        for i in calc_dict['fields']:
            calc_embed.add_field(name = i['name'], value = i['value'], inline = False)
        calc_embed.add_field(name = f'race{len(calc_dict["fields"]) + 1} ' + run_track, value = value, inline = False)
    return calc_embed


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
    
    mc = message.content
    channel = message.channel
    
    # calc_bot
    if mc == 'calc':
        calc_embed = discord.Embed(title = '即時集計 6v6', description = '0 : 0 @12', color = 0xd2cab6)
        await channel.send(embed = calc_embed)
    
    elif mc.startswith('calc') and ' ' in mc:
        vs_list = list(mc.split(' '))
        if not len(vs_list) in [2,3,4,6]:
            await channel.send('チーム数おかしいかも:cry:')
        else:
            title_text = f'即時集計 {12//len(vs_list)}v{12//len(vs_list)}\nvs'
            description_text = '0'
            for i in vs_list[1:]:
                title_text += f' {i}'
                description_text += ' : 0'
            description_text += ' @12'
            calc_embed = discord.Embed(title = title_text, description = description_text, color = 0xd2cab6)
            await channel.send(embed = calc_embed)

    elif str.isdecimal(mc.replace(' ','')) or mc == 'back':
        calc_dict = None
        calc_support_dict = None
        run_track = ''
        messages = await channel.history(after = datetime.utcnow() - timedelta(minutes = 15)).flatten()
        for i in reversed(messages):
            if i.author.name == 'sneet' and i.author.discriminator == '1219':
                i_dict = i.embeds[0].to_dict()
                if 'image' in i_dict and i_dict['image']['url'].startswith('https://raw.githubusercontent.com/sheat-git/mk8dx/main/files/') and run_track == '':
                    run_track = ' (' + i_dict['title'] + ')'
                elif i_dict['title'].startswith('race') and calc_support_dict == None:
                    delete_message_2 = i
                    calc_support_dict = i_dict
                    calc_support_embed = i.embeds[0].copy()
                elif i_dict['title'].startswith('即時集計'):
                    delete_message = i
                    calc_dict = i_dict
                    match_type = int(i_dict['title'][5])
                    break
        if calc_dict == None:
            pass
        elif mc == 'back':
            if calc_support_dict == None:
                score_list = list(map(lambda x: -int(x.split(' (')[0]), calc_dict['fields'][-1]['value'].split(' |')[0].split(' : ')))
                sum_score_list = calc_sum_score(' : '.join(list(map(lambda x: str(x.split(' (')[0]), calc_dict['description'].split(' @')[0].split(' : ')))), score_list)
                calc_embed = discord.Embed(title = calc_dict['title'], description = ' : '.join(map(str, sum_score_list)) + f' @{int(calc_dict["description"].split(" @")[1]) + 1}', color = 0xd2cab6)
                for i in calc_dict['fields'][:-1]:
                    calc_embed.add_field(name = i['name'], value = i['value'], inline = False)
                await channel.send(embed = calc_embed)
                await delete_message.delete()
            else:
                await delete_message_2.delete()
        elif 'fields' in calc_dict and len(calc_dict["fields"]) >= 12:
            pass
        elif match_type != 6 and not ' ' in mc:
            send_status_2 = False
            rs_list = calc_score(match_type, [mc])
            rank_list = rs_list[0]
            score_list = rs_list[1]
            team_list = list(calc_dict['title'].split('vs ')[1].split(' '))
            if len(rank_list) != match_type:
                pass
            elif calc_support_dict == None:
                if 'fields' in calc_dict:
                    title = f'race{len(calc_dict["fields"]) + 1}'
                else:
                    title = 'race1'
                calc_support_embed = discord.Embed(title = title + ' ' + run_track, color = 0xd2cab6)
                calc_support_embed.add_field(name = 'Your team', value = f'score : {score_list[0]} | rank : {",".join(list(rank_list))}', inline = False)
                rank_text = '0'
                for i in range(match_type-1):
                    rank_text += ',0'
                for team in team_list:
                    calc_support_embed.add_field(name = team, value = f'score : 0 | rank {rank_text}', inline = False)
                await channel.send(embed = calc_support_embed)
            else:
                send_status = False
                rank_list_ever = []
                for i in range(12//match_type):
                    if calc_support_dict['fields'][i]['value'][-2:] == ',0':
                        if len(set(rank_list_ever) & set(rank_list)) >= 1:
                            pass
                        else:
                            calc_support_embed.set_field_at(i, name = calc_support_dict['fields'][i]['name'], value = f'score : {score_list[0]} | rank : {",".join(list(rank_list))}', inline = False)
                            rank_list_ever += rank_list
                            send_status = True
                        if i == 12 // match_type - 2 and send_status:
                            rank_list_never = list({'1','2','3','4','5','6','7','8','9','10','11','12'}-set(rank_list_ever))
                            rank_list_never = sorted(list(map(int, rank_list_never)))
                            rank_list_never = list(map(str, rank_list_never))
                            calc_support_embed.set_field_at(i+1, name = calc_support_dict['fields'][i+1]['name'], value = f'score : {calc_score(match_type, ["".join(rank_list_never)])[1][0]} | rank : {",".join(rank_list_never)}', inline = False)
                            send_status_2 = True
                        break
                    else:
                        rank_list_ever += list(calc_support_dict['fields'][i]['value'].split('rank : ')[-1].split(','))
                if send_status:
                    await channel.send(embed = calc_support_embed)
                    await delete_message_2.delete()
            if send_status_2:
                mc_text = ''
                for i in range(12//match_type - 2):
                    mc_text += calc_support_dict['fields'][i]['value'].split('rank : ')[-1].replace(',','') + ' '
                mc_text += ''.join(rank_list)
                calc_embed = create_calc_embed(match_type, mc_text, calc_dict, run_track)
                await channel.send(embed = calc_embed)
                await delete_message.delete()
        else:
            calc_embed = create_calc_embed(match_type, mc, calc_dict, run_track)
            await channel.send(embed = calc_embed)
            await delete_message.delete()

    else:
        # track_bot
        send_track_list = search_track(mc)
        if not send_track_list == None:
            track_embed = discord.Embed(title = send_track_list[0].replace(':',' '), color = 0xd2cab6)
            track_embed.set_image(url = send_track_list[1])
            await channel.send(embed = track_embed)
        send_tracks_list = search_tracks(mc)
        if not send_tracks_list == None:
            description = ''
            for i in send_tracks_list[1]:
                description += search_track(i)[0].replace(':', ' ') + '\n'
            tracks_embed = discord.Embed(title = send_tracks_list[0], description = description[:-1], color = 0xd2cab6)
            await channel.send(embed = tracks_embed)
        
        # function
        if mc in ['func', '"func"', "''func''"]:
            func_embed = discord.Embed(title = '機能説明', color = 0xd2cab6)
            func_embed.set_author(name="twitter:@sheat_MK", url="https://twitter.com/sheat_MK", icon_url="https://pbs.twimg.com/profile_images/1315419578646708224/DqNBLGeY_400x400.jpg")
            func_embed.add_field(name = 'コース名  (例:`ベビぱ`)', value = 'コース名の略称から英語名・日本語名をフルで返答します\n全てのコース名に反応するのでチャンネルに応じてこのbotの「メッセージを読む」権限を剥奪してください\n** **', inline=False)
            func_embed.add_field(name = '即時集計  (例:`calc BP`)', value = 'calc で始めることができます\n`calc` : 6v6\n`calc tag1` : tag1との6v6\n`calc tag1 tag2` : tag1,tag2との4v4\n`calc tag1 tag2 tag3`\n : tag1,tag2,tag3との3v3\n`calc tag1 tag2 tag3 tag4 tag5`\n : tag1-tag5との2v2\n点数入力は2通りできます\n**1.チームごとに空白区切り**\n\t`123 456 789`\n\t上記のようにしてあなたのチーム,tag1,tag2の順に入力します\n\t最後のチームの点数は補完されます\n**2.チームごとに送信**\n\t`123`\n\t`456`\n\t`789`\n\t上記のように順に送信してください\n\t1と同様に最後のチームは補完されます\n** **', inline=False)
            func_embed.add_field(name = '即時集計のコース記録', value = '前回の即時の入力から次回集計までに入力されたコースのうち、最新のものを記録していきます', inline=False)
            await channel.send(embed = func_embed)

# Botの起動とDiscordサーバーへの接続
if __name__ == '__main__':
    client.run(TOKEN)

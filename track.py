import discord
import os

from discord.ext.commands.errors import NoEntryPointError


ORIGINAL_COLOR = int(os.environ['COLOR'],0)


def search(name):
    name = str.lower(name)
    rDKJ_list = ['rDKJ', 'rdkj', 'dkj', 'じゃんぐる', 'ジャングル', 'jk', 'JK', 'dk']
    rPPS_list = ['rPPS', 'rpps', 'pps', 'パクスラ', 'パックンスライダー', 'ぱくすら', 'ぱっくんすらいだー', 'パックン', 'ぱっくん']
    rMP_list = ['rMP', 'rmp', 'mp', 'ミュージックパーク', 'ミューパ', 'ミューぱ', 'みゅーじっくぱーく', 'みゅーぱ', 'seimei']
    rTTC_list = ['rTTC', 'rttc', 'ttc', 'チクタクロック', 'チクタク', 'ティックトック', 'チックタック', 'ちっくたっく', 'ちくたくろっく', 'ちくたく', 'てぃっくとっく']
    rCCB_list = ['rCCB', 'rccb', 'ccb', 'プクプクビーチ', 'プクプク', 'プクビ', 'ぷくぷくびーち', 'ぷくぷく', 'ぷくび', 'びーち', 'ビーチ']
    rWS_list = ['rWS', 'rws', 'ws', 'ワリオスタジアム', 'ワリスタ', 'わりすた', 'わりおすたじあむ']
    rMC_list = ['rMC', 'rmc', 'RMC', 'GBA', 'ぐば', 'グバ', 'GBAまりさ', 'GBAマリサ', 'GBAマリオサーキット', 'GBAまりおさーきっと', 'ジービーエー', 'ジビエ', 'じーびーえー', 'じびえ', 'gba']
    rDDD_list = ['rDDD', 'rddd', 'RDDD', 'カラカラ', 'カラサバ', 'からさば', 'からから', 'カラカラ砂漠', 'からからさばく', 'カラカラさばく', 'カラカラサバク']
    rSL_list = ['rSL', 'rsl', 'sl', 'しゃべらん', 'シャベラン', 'シャーベットランド', 'しゃーべっとらんど', 'シャーベット', 'しゃーべっと']
    dYC_list = ['dYC', 'dyc', 'DYC', 'ヨシサ', 'ヨッシーサーキット', 'よしさ', 'よっしーさーきっと']
    rTT_list = ['rTT', 'rtt', 'tt', 'キノピオハイウェイ', '高速道路', '高速', 'こうそくどうろ', 'こうそく', 'はいうぇい', 'ハイウェイ', 'きのぴおはいうぇい']
    rRRy_list = ['rRRy', 'rrry', 'RRRY', 'ピーチサーキット', 'ぴーちさーきっと', 'ピチさ', 'ピチサ', 'ぴちさ']
    rYV_list = ['rYV', 'ryv', 'yv', 'ヨシバ', 'よっしーバレー', 'よっしーばれー', 'ヨッシーバレー', 'よしば', 'バレー', 'ばれー']
    rRRd_list = ['rRRd', 'rrrd', 'RRRD', '64虹', '６４虹', '64にじ', '６４にじ', 'ろくよん', 'ロクヨン']
    rDP3_list = ['rDP3', 'rdp3', 'dp3', 'ドーナツへいや', 'どーなつへいや', 'ドーナツ平野', 'どーなつ平野', 'ドーナツヘイヤ', '平野', 'へいや']
    dRR_list = ['dRR', 'drr', 'DRR', 'SFC', 'sfc', 'SFCにじ', 'SFC虹', 'sfcにじ', 'sfc虹', 'えすえふしー', 'エスエフシー', 'SFCレインボーロード', 'sfcレインボーロード', 'SFCれいんぼーろーど', 'sfcれいんぼーろーど', 'えすえふしーにじ', 'エスエフシーニジ']
    rGV_list = ['rGV', 'rgv', 'gv', 'ぐらぐら', 'グラグラ', 'グラグラ火山', 'ぐらぐら火山', 'グラグラカザン', 'ぐらぐらかざん', '火山', 'かざん']
    rMMM_list = ['rMMM', 'rmmm', 'mmm', 'モモカン', 'もーもーカントリー', 'モーモーカントリー', 'ももかん', 'もーもーかんとりー', '牛', 'うし', 'わたがし']
    dWGM_list = ['dWGM', 'dwgm', 'DWGM', 'ワリオこうざん', 'ワリオ鉱山', 'わりおこうざん', 'わりこう', 'ワリこう', 'ワリ鉱', 'わり鉱', 'gomi', 'gomi track']
    WP_list = ['WP', 'wp', 'ウォーターパーク', 'ヲーターパーク', 'うぉーたーぱーく', 'をーたーぱーく', 'をたぱ', 'ヲタパ', 'うぉたぱ', 'ウォタパ', '水公園', 'オタぱ', 'おたぱ', 'オタパ']
    dEA_list = ['dEA', 'dea', 'DEA', 'エキサイトバイク', '役馬', 'エキバ', 'えきば', 'えきさいとばいく']
    Ed_list = ['Ed', 'ed', 'ED', 'エレドリ', 'エレド', 'エレクトロドリーム', 'えれどり', 'えれど', 'えれくとろどりーむ', '夢']
    TH_list = ['TH', 'th', 'キノピオハーバー', 'きのぴおはーばー', 'はーばー', 'ハーバー', 'せいめい']
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
    SGF_list = ['SGF', 'sgf', 'へいほーこうざん', 'ヘイホー鉱山', 'ヘイホーこうざん', 'へいほー鉱山', 'へいこう', 'ヘイコウ', 'へい鉱', 'ヘイ鉱', 'ヘイこう']
    BDD_list = ['BDD', 'bdd', 'ホネホネさばく', 'ホネホネ砂漠', 'ほねほねさばく', 'ほねほね砂漠', '骨骨砂漠', '骨骨さばく', 'ホネホネサバク', 'ほねさば', '骨サバ', 'ホネサバ', '骨', 'ほね', 'ホネ', 'ほねほね', '骨骨', 'ホネホネ']
    MKS_list = ['MKS', 'mks', 'マリオカートスタジアム', 'まりおかーとすたじあむ', 'マリカす', 'マリカス', 'まりかす']
    MC_list = ['MC', 'mc', 'マリオサーキット', 'マリサ', 'まりおさーきっと', 'まりさ', '新マリサ', 'しんまりさ', 'シンマリサ', '新まりさ']
    RR_list = ['RR', 'rr', '新虹', 'しんにじ', 'レインボーロード', 'シンニジ', 'れいんぼーろーど']
    dMC_list = ['dMC', 'dmc', 'DMC', 'ミュートシティ', 'ミュート', 'みゅーと', 'みゅーとしてぃ']
    dBP_list = ['dBP', 'dbp', 'DBP', 'BP', 'bp', 'ベビィパーク', 'ベビーパーク', 'べびぃぱーく', 'べびーぱーく', 'べびぱ', 'ベビパ', 'kami', 'kami track', 'おみくじこーす']
    dCL_list = ['dCL', 'dcl', 'DCL', 'チーズランド', 'ちーずらんど', 'ちーず', 'チーズ']
    dWW_list = ['dWW', 'dww', 'DWW', 'ネイチャーロード', 'ねいちゃーろーど', 'ネイチャー', 'ねいちゃー', 'なちゅれ', 'ナチュレ']
    dAC_list = ['dAC', 'dac', 'DAC', 'ac', 'AC', 'どうぶつの森', 'どうもり', '動物の森', 'どう森', 'ぶつ森', 'ぶつもり', 'ドウブツノモリ', 'ドウモリ', 'ブツモリ']
    dNBC_list = ['dNBC', 'dnbc', 'DNBC', 'ネオクッパシティ', 'ねおくっぱしてぃ', 'ネオぱ', 'ネオパ', 'ねおぱ', 'ねおくっぱ', 'ネオクッパ']
    dRiR_list = ['dRiR', 'DRIR', 'drir', 'リボンロード', 'リボン', 'りぼんろーど', 'りぼん']
    dSBS_list = ['dSBS', 'dsbs', 'DSBS', 'リンリンメトロ', 'りんりんめとろ', 'りんめと', 'リンメト', 'リンリン', 'りんりん', 'リン', 'りん', '凛']
    dBB_list = ['dBB', 'dbb', 'bb', 'ビッグブルー', 'びっぐぶるー', 'もざびー']
    MW_list = ['MW', 'mw', 'ワリオスノーマウンテン', 'わりおすのーまうんてん', 'ワリスノ', 'わりすの', '雪山', 'ゆきやまうんてん', 'すの', 'スノ']
    tracks_list = [ \
        [['MKS:マリオカートスタジアム', MKS_list], ['WP:ウォーターパーク', WP_list], ['SSC:スイーツキャニオン', SSC_list], ['TR:ドッスンいせき', TR_list]], \
        [['MC:新マリオサーキット', MC_list], ['TH:キノピオハーバー', TH_list], ['TM:ねじれマンション', TM_list], ['SGF:ヘイホーこうざん', SGF_list]], \
        [['SA:サンシャインくうこう', SA_list], ['DS:ドルフィンみさき', DS_list], ['Ed:エレクトロドリーム', Ed_list], ['MW:ワリオスノーマウンテン', MW_list]], \
        [['CC:スカイガーデン', CC_list], ['BDD:ホネホネさばく', BDD_list], ['BC:クッパキャッスル', BC_list], ['RR:新レインボーロード', RR_list]], \
        [['dYC:ヨッシーサーキット', dYC_list], ['dEA:エキサイトバイク', dEA_list], ['dDD:ドラゴンロード', dDD_list], ['dMC:ミュートシティ', dMC_list]], \
        [['dBP:ベビィパーク', dBP_list], ['dCL:チーズランド', dCL_list], ['dWW:ネイチャーロード', dWW_list], ['dAC:どうぶつの森', dAC_list]], \
        [['rMMM:モーモーカントリー', rMMM_list], ['rMC:GBAマリオサーキット', rMC_list], ['rCCB:プクプクビーチ', rCCB_list], ['TT:キノピオハイウェイ', rTT_list]], \
        [['rDDD:カラカラさばく', rDDD_list], ['rDP3:ドーナツへいや', rDP3_list], ['rRRy:ピーチサーキット', rRRy_list], ['rDKJ:DKジャングル', rDKJ_list]], \
        [['rWS:ワリオスタジアム', rWS_list], ['rSL:シャーベットランド', rSL_list], ['rMP:ミュージックパーク', rMP_list], ['rYV:ヨッシーバレー', rYV_list]], \
        [['rTTC:チクタクロック', rTTC_list], ['rPPS:パックンスライダー', rPPS_list], ['rGV:グラグラかざん', rGV_list], ['rRRd:64レインボーロード', rRRd_list]], \
        [['dWGM:ワリオこうざん', dWGM_list], ['dRR:SFCレインボーロード', dRR_list], ['dIIO:ツルツルツイスター', dIIO_list], ['dHC:ハイラルサーキット', dHC_list]], \
        [['dNBC:ネオクッパシティ', dNBC_list], ['dRiR:リボンロード', dRiR_list], ['dSBS:リンリンメトロ', dSBS_list], ['dBB:ビッグブルー', dBB_list]]]
    for i in range(12):
        for j in range(4):
            if name in tracks_list[i][j][1]:
                return [tracks_list[i][j][0], f'https://raw.githubusercontent.com/sheat-git/mk8dx/main/files/{i+1}.JPG']

def type_search(name):
    front = ['前コース', '前コ', '前こ', '前', '前個', 'まえこ', 'まえ', 'まえこーす']
    mid = ['中位コース', '中位コ', '中位こ', '中位', '中', 'なか', 'ちゅうい', 'ちゅういこ', 'ちゅういこーす']
    back = ['打開コース', '打開コ', '打開こ', 'だかいこ', '打開', 'だかいこーす', 'だかい', 'うしろ', '後', '後ろ']
    strategy_dict = {'前コース':['WS', 'dNBC', 'DKJ', 'dHC', 'MW', 'TTC'], '中位コース':['TM', 'Ed', 'DS', 'dIIO', 'MP', 'MMM'], '打開コース':['dCL', 'rDDD', 'dEA', 'YV', 'rMC', 'DP3']}
    for i in [front, mid, back]:
        if name in i:
            return [i[0],strategy_dict[i[0]]]

def embed(txt):
    global ORIGINAL_COLOR
    track_list = search(txt)
    if not track_list == None:
        embed = discord.Embed(title = track_list[0].replace(':',' '), color = ORIGINAL_COLOR)
        embed.set_image(url = track_list[1])
        return embed
    type_list = type_search(txt)
    if not type_list == None:
        embed = discord.Embed(title = type_list[0], description = '\n'.join(map(lambda x:search(x)[0].replace(':',' '), type_list[1])), color=ORIGINAL_COLOR)
        return embed
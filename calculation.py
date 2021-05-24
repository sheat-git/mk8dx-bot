import discord
import string
from PIL import Image
from typing import Type, TypeVar
import io
import json
import os

import function as func
import track
import fbrtdb
import mkresult


ORIGINAL_COLOR = int(os.environ['COLOR'],0)


T = TypeVar('T', bound='table')
sT = TypeVar('sT', bound='subTable')


class table:
    def __init__(self,form=6,teams=[],sum=[0,0],scores=[],ranks=[],tracks=[],obs=set()):
        self.form = form
        if 12//form == len(teams):
            self.teams = teams
        elif 12//form > len(teams):
            first_teams = []
            for i in range(12//form - len(teams)):
                first_teams.append(string.ascii_uppercase[i] *2)
            self.teams = first_teams + teams
        else:
            self.teams = teams[:12//form]
        if scores == []:
            self.sum = [0] * (12//form)
        else:
            self.sum = sum
        self.scores = scores
        self.ranks = ranks
        self.tracks = tracks
        self.obs = obs
    
    def __int__(self):
        return len(self.scores)
    
    def __len__(self):
        return len(self.teams)
    
    def add(self,score,rank,track=''):
        for i in range(len(self)):
            self.sum[i] += score[i]
        self.scores.append(score)
        self.ranks.append(rank)
        self.tracks.append(track)
    
    def back(self):
        if int(self) == 0:
            return self
        for i in range(len(self)):
            self.sum[i] -= self.scores[-1][i]
        del self.scores[-1]
        del self.ranks[-1]
        del self.tracks[-1]
    
    def addTxt(self,txt,track=''):
        if self.form != 6:
            return
        rank = txt2rank(txt)
        if len(rank) >=  6:
            rank = rank[:6]
        elif len(rank) < 6:
            rank = fillRank(rank,form=6)
        s = calcScore(rank)
        self.add([s,82-s],rank,track)
    
    def addStbl(self,stbl):
        self.add(stbl.scores, stbl.ranks[0], stbl.track)

    @classmethod
    def fromDict(cls:Type[T],embed_dict) -> T:
        self: T = cls.__new__(cls)
        self.form = int(embed_dict['title'][5])
        self.teams = list(embed_dict['title'].split('\n')[-1].split(' - '))
        self.sum = list(map(lambda x: int(x.split('(')[0]), embed_dict['description'].replace('`','').split('  @')[0].split(' : ')))
        if 'footer' in embed_dict:
            self.obs = set(embed_dict['footer']['text'].replace('OBS for @','').split(',@'))
        else:
            self.obs = set()
        self.scores = []
        self.ranks = []
        self.tracks = []
        if 'fields' in embed_dict:
            for field in embed_dict['fields']:
                value = field['value'].replace('`','')
                self.scores.append(list(map(lambda x: int(x.split('(')[0]), value.split(' | ')[0].split(' :'))))
                self.ranks.append(list(map(int, value.split(' | ')[1].split(','))))
                if '  - ' in field['name']:
                    self.tracks.append(field['name'].split('  - ')[1])
                else:
                    self.tracks.append('')
        return self
    
    @classmethod
    def fromEmbed(self,embed):
        return self.fromDict(embed.to_dict())
    
    @classmethod
    def fromEmbeds(self,embeds):
        return self.fromEmbed(embeds[0])
    
    @classmethod
    def fromMessage(self,message):
        return self.fromEmbeds(message.embeds)

    def _score2txt(self,score):
        score_txt = ''
        for i,s in enumerate(score):
            if i == 0:
                score_txt += str(s)
            else:
                if self.form == 2:
                    score_txt += ' : ' + str(s)
                else:
                    score_txt += ' : {}({:+})'.format(s,score[0]-s)
        return score_txt

    def toDict(self):
        global ORIGINAL_COLOR
        title = f'即時集計 {self.form}v{self.form}\n' + ' - '.join(self.teams)
        description = f'`{self._score2txt(self.sum)}`  `@{12 - len(self.scores)}`'
        fields = []
        for i, (score, rank, track) in enumerate(zip(self.scores, self.ranks, self.tracks)):
            field = {}
            field['name'] = f'race{i+1}'
            if track:
                field['name'] += f'  - {track}'
            field['value'] = f'`{self._score2txt(score)}` | `{",".join(map(str,rank))}`'
            field['inline'] = False
            fields.append(field)
        if len(self.obs) > 0:
            footer = {'text': 'OBS for @' + ',@'.join(self.obs)}
            return {'title':title, 'description':description, 'fields':fields, 'color':ORIGINAL_COLOR, 'footer':footer}
        else:
            return {'title':title, 'description':description, 'fields':fields, 'color':ORIGINAL_COLOR}
    
    def toEmbed(self):
        return discord.Embed.from_dict(self.toDict())


class subTable:
    def __init__(self,form=2,teams=[],race=1,scores=[],ranks=[],track=''):
        self.race = race
        self.form = form
        if 12//form == len(teams):
            self.teams = teams
        elif 12//form > len(teams):
            first_teams = []
            for i in range(12//form - len(teams)):
                first_teams.append(string.ascii_uppercase[i] *2)
            self.teams = first_teams + teams
        else:
            self.teams = teams[:12//form]
        if 12//form == len(scores):
            self.scores = scores
        elif 12//form > len(scores):
            self.scores = scores + [0] * (12//form - len(scores))
        else:
            self.scores = scores[:12//form]
        if 12//form == len(ranks):
            self.ranks = ranks
        elif 12//form > len(ranks):
            self.ranks = ranks
            for _ in range(12//form - len(ranks)):
                self.ranks.append([0]*form)
        else:
            self.ranks = ranks[:12//form]
        self.track = track
    
    def __int__(self):
        return self.race
    
    def __len__(self):
        return len(self.teams)
    
    def filled(self):
        c = 0
        for score in self.scores:
            if score == 0:
                break
            c += 1
        return c
    
    def add(self,scores,ranks,track=''):
        preScores = self.scores
        self.scores = []
        i = 0
        for preScore in preScores:
            if len(scores) == i:
                self.scores.append(preScore)
            elif preScore == 0:
                self.scores.append(scores[i])
                i += 1
            else:
                self.scores.append(preScore)
        preRanks = self.ranks
        self.ranks = []
        i = 0
        for preRank in preRanks:
            if len(ranks) == i:
                self.ranks.append(preRank)
            elif 0 in preRank:
                self.ranks.append(ranks[i])
                i += 1
            else:
                self.ranks.append(preRank)
        if track:
            self.track = track
    
    def update(self,scores,ranks,track=''):
        self.scores = scores
        self.ranks = ranks
        if track:
            self.track = track
    
    def back(self):
        filled = self.filled()
        if filled == 1:
            return self
        self.scores[filled-1] = 0
        self.ranks[filled-1] = [0]*self.form
    
    def addTxt(self,txt):
        ranks = multiTxt2ranks(self.form, txt, self.ranks[:])
        if not ranks:
            return False
        scores = calcScores(ranks)
        while len(ranks) < len(self):
            ranks.append([0]*self.form)
        while len(scores) < len(self):
            scores.append(0)
        self.update(scores,ranks)
        return True

    @classmethod
    def fromDict(cls:Type[sT],embed_dict) -> sT:
        self: sT = cls.__new__(cls)
        self.race = int(embed_dict['title'].replace('race','').split('  - ')[0])
        self.form = 12//len(embed_dict['fields'])
        self.teams = []
        self.scores = []
        self.ranks = []
        for field in embed_dict['fields']:
            self.teams.append(field['name'])
            value = field['value'].replace('`','')
            self.scores.append(int(value.split(' | ')[0].split(': ')[1]))
            self.ranks.append(list(map(int, value.split(' | ')[1].split(': ')[1].split(','))))
        if '  - ' in embed_dict['title']:
            self.track = embed_dict['title'].split('  - ')[1]
        else:
            self.track = ''
        return self
    
    @classmethod
    def fromEmbed(self,embed):
        return self.fromDict(embed.to_dict())
    
    @classmethod
    def fromEmbeds(self,embeds):
        return self.fromEmbed(embeds[0])
    
    @classmethod
    def fromMessage(self,message):
        return self.fromEmbeds(message.embeds)
    
    @classmethod
    def mkFromTbl(cls:Type[sT],tbl,track='') -> sT:
        self: sT = cls.__new__(cls)
        self.race = int(tbl) + 1
        self.form = tbl.form
        self.teams = tbl.teams
        self.scores = [0] * (12//self.form)
        self.ranks = []
        for _ in range(len(self)):
            self.ranks.append([0]*self.form)
        self.track = track
        return self
    
    def toDict(self):
        global ORIGINAL_COLOR
        title = 'race' + str(self.race)
        if self.track:
            title += f'  - {self.track}'
        fields = []
        for team,score,rank in zip(self.teams, self.scores, self.ranks):
            field = {}
            field['name'] = team
            field['value'] = f'score : `{score}` | rank : `{",".join(map(str, rank))}`'
            field['inline'] = False
            fields.append(field)
        return {'title':title, 'fields':fields, 'color':ORIGINAL_COLOR}
    
    def toEmbed(self):
        return discord.Embed.from_dict(self.toDict())


def is16int(s):
    try:
        int(s,16)
        return True
    except ValueError:
        return False

def is13int(s):
    if len(set(s) & {'d','e','f'}) > 1:
        return False
    elif is16int(s):
        return True
    else:
        return False

def txt2rank(txt):
    rank_txt = ''.join(map(lambda x:str(int(x,16)) if is16int(x) else x, txt))
    if rank_txt.startswith('-'):
        rank_txt = '1' + rank_txt
    if rank_txt.endswith('-'):
        rank_txt += '12'
    rank_charList = list(rank_txt)
    rank = []
    i = 0
    while len(rank_charList) > i:
        char = rank_charList[i]
        if char == '1':
            if len(rank_charList) > i+1:
                nextChar = rank_charList[i+1]
                if nextChar == '-':
                    rank.append(int(char))
                elif not nextChar in ['0','1'] and i == 0:
                    rank.append(1)
                else:
                    rank.append(int(char + nextChar))
                    i += 1
            else:
                rank.append(int(char))
        elif char == '0':
            rank.append(10)
        elif char == '-':
            nextChar = rank_charList[i+1]
            if nextChar == '0':
                next = 10
                i += 1
            elif nextChar == '1':
                if len(rank_charList) > i+2:
                    next = int(nextChar + rank_charList[i+2])
                    i += 2
                else:
                    next = 11
                    i += 1
            else:
                next = int(nextChar)
                i += 1
            prev = rank[-1]
            while prev < next:
                prev += 1
                rank.append(prev)
        else:
            rank.append(int(char))
        i += 1
    rank = sorted(set(rank))
    return [i for i in rank if 0<i<13]


def fillRank(rank,form=0,never = {1,2,3,4,5,6,7,8,9,10,11,12}):
    if not form:
        return
    if len(rank) >= form:
        return rank[:form]
    never = set(never)
    never -= set(rank)
    if len(never) + len(rank) < form:
        return
    while len(rank) < form:
        add = max(never)
        rank.append(add)
        never -= {add}
    return sorted(rank)
    

def multiTxt2ranks(form, rank_multiTxt, ranks):
    never = {1,2,3,4,5,6,7,8,9,10,11,12}
    for i in reversed(range(len(ranks))):
        rank = ranks[i]
        if 0 in rank:
            del ranks[i]
        else:
            never -= set(rank)
    for rank_txt in rank_multiTxt.split(' '):
        rank = txt2rank(rank_txt)
        if len(rank) > form:
            new_rank = []
            for r in rank:
                if r in never:
                    new_rank.append(r)
                if len(new_rank) == form:
                    break
            rank = new_rank
        else:
            rank = fillRank(rank,form,never)
        if not check_rank(form, rank, never):
            return False
        elif len(ranks) < 12//form:
            ranks.append(rank)
            never -= set(rank)
    if len(never) == form:
        ranks.append(sorted(list(never)))
    return ranks


def calcScore(rank):
    scoreDict = {1:15,2:12,3:10,4:9,5:8,6:7,7:6,8:5,9:4,10:3,11:2,12:1,0:0}
    score = 0
    for r in rank:
        score += scoreDict[r]
    return score


def calcScores(ranks):
    scores = []
    for rank in ranks:
        scores.append(calcScore(rank))
    return scores


def check_rank(form, rank, never):
    if rank == None:
        return False
    elif form != len(rank):
        return False
    elif not len(set(rank) & never) == form:
        return False
    else:
        return True

def isTrack(embed,embed_dict=None):
    if embed == None:
        if not 'image' in embed_dict:
            return False
        elif not 'url' in embed_dict['image']:
            return False
        url = embed_dict['image']['url']
    else:
        url = embed.image.url
    if type(url) is discord.embeds._EmptyEmbed:
        return False
    elif url.startswith('https://raw.githubusercontent.com/sheat-git/mk8dx/main/files/'):
        return True
    else:
        return False

def isSubTable(embed,embed_dict=None):
    if embed == None:
        if not 'title' in embed_dict:
            return False
        title = embed_dict['title']
    else:
        title = embed.title
    if type(title) is discord.embeds._EmptyEmbed:
        return False
    if title.startswith('race'):
        return True
    else:
        return False

def isTable(embed,embed_dict=None):
    if embed == None:
        if not 'title' in embed_dict:
            return False
        title = embed_dict['title']
    else:
        title = embed.title
    if type(title) is discord.embeds._EmptyEmbed:
        return False
    if title.startswith('即時集計 ') and not title.endswith(' START!') and '\n' in title:
        return True
    else:
        return False

def search(messages, author=None):
    mg = None
    smg = None
    track = ''
    for message in reversed(messages):
        if message.author == author and len(message.embeds) != 0:
            embed = message.embeds[0]
            if isTrack(embed) and track == '':
                track = embed.title.split(' ')[0]
            elif isSubTable(embed) and smg == None:
                smg = message
            elif isTable(embed):
                mg = message
                break
    return [mg,smg,track]


def start(ctx, args, form=0):
    teams = list(args)
    if ctx.guild == None:
        name = ctx.author.name
    else:
        name = ctx.guild.name
    if len(name) > 5:
        name = name[:5]
    c = len(teams)
    if not form:
        caln = 0
        if c <= 2:
            if c == 1:
                teams = [name] + teams
            tbl = table(form=6,teams=teams)
        elif c == 3:
            tbl = table(form=4,teams=teams)
        elif c == 4:
            tbl = table(form=3,teams=teams)
        elif c <= 6:
            if c == 5:
                teams = [name] + teams
            tbl = table(form=2,teams=teams)
    else:
        caln = form
        if 12//form == c+1:
            teams = [name] + teams
        tbl = table(form=form,teams=teams)
    return [func.calStartEmbed(teams=tbl.teams,form=tbl.form,caln=caln,args=args),tbl.toEmbed()]


def setTeams(ctx, args, messages, author=None):
    teams = list(args)
    message = search(messages, author)[0]
    if message == None:
        return {}
    tbl = table.fromMessage(message)
    if len(tbl) == len(teams):
        tbl.teams = teams
    elif len(tbl) == len(teams) + 1:
        if ctx.guild == None:
            name = ctx.author.name
        else:
            name = ctx.guild.name
        if len(name) > 5:
            name = name[:5]
        tbl.teams = [name] + teams
    elif len(tbl) > len(teams):
        first_teams = []
        for i in range(len(tbl) - len(teams)):
            first_teams.append(string.ascii_uppercase[i] *2)
        tbl.teams = first_teams + teams
    else:
        tbl.teams = teams[:len(tbl)]
    return {'embeds':[tbl.toEmbed()], 'del':[message]}


def cal(content,messages, author=None):
    tbl_mg, stbl_mg, track = search(messages,author)
    if tbl_mg == None:
        return {}
    tbl = table.fromMessage(tbl_mg)
    if int(tbl) == 12:
        return {}
    if tbl.form != 6:
        if stbl_mg == None:
            stbl = subTable.mkFromTbl(tbl, track)
        else:
            stbl = subTable.fromMessage(stbl_mg)
        if not stbl.addTxt(content):
            return {}
        if stbl.filled() == 12//tbl.form:
            tbl.addStbl(stbl)
            returnDict =  {'embeds':[stbl.toEmbed(), tbl.toEmbed()],'del':[tbl_mg]}
        else:
            returnDict =  {'embeds':[stbl.toEmbed()],'del':[]}
        if stbl_mg == None:
            return returnDict
        else:
            returnDict['del'].append(stbl_mg)
            return returnDict
    tbl.addTxt(content,track)
    return {'embeds':[tbl.toEmbed()],'del':[tbl_mg]}


def back(messages,author=None):
    tbl_mg, stbl_mg, track = search(messages,author)
    if not stbl_mg == None:
        stbl = subTable.fromMessage(stbl_mg)
        if stbl.filled() > 1:
            stbl.back()
            return {'embeds':[stbl.toEmbed()],'del':[stbl_mg]}
        else:
            return {'del':[stbl_mg]}
    elif not tbl_mg == None:
        tbl = table.fromMessage(tbl_mg)
        tbl.back()
        return {'embeds':[tbl.toEmbed()],'del':[tbl_mg]}


def edit():
    pass

def result(ctx,messages,author=None):
    tbl_mg, stbl_mg, track = search(messages,author)
    if tbl_mg == None:
        return
    tbl = table.fromMessage(tbl_mg)
    if tbl.form != 6 or int(tbl) < 12:
        return
    sum = tbl.sum
    teams = tbl.teams
    difs = [0]*int(tbl)
    if sum[0] < sum[1]:
        sum.reverse()
        teams.reverse()
        for i,score in enumerate(tbl.scores):
            difs[i] = score[1] - score[0]
            if i > 0:
                difs[i] += difs[i-1]
    else:
        for i,score in enumerate(tbl.scores):
            difs[i] = score[0] - score[1]
            if i > 0:
                difs[i] += difs[i-1]
    img = mkresult.make6(difs,sum,teams)
    image_binary = io.BytesIO()
    img.save(image_binary,'png')
    image_binary.seek(0)
    imgDFile = discord.File(fp=image_binary,filename='result.png')
    image_binary.close()
    jsonData = {'type':'result','id':ctx.channel.id,'teams':teams,'sum':sum}
    return [imgDFile,json.dumps(jsonData)]

def send(channel,messages,author=None):
    tbl_mg, stbl_mg, track = search(messages,author)
    if tbl_mg == None:
        return
    tbl = table.fromMessage(tbl_mg)
    if tbl.form != 6 or int(tbl) < 12:
        return
    sum = tbl.sum
    teams = tbl.teams
    difs = [0]*int(tbl)
    for i,score in enumerate(tbl.scores):
        difs[i] = score[0] - score[1]
        if i > 0:
            difs[i] += difs[i-1]
    img = mkresult.make6(difs,sum,teams)
    image_binary = io.BytesIO()
    img.save(image_binary,'png')
    image_binary.seek(0)
    imgDFile = discord.File(fp=image_binary,filename='result.png')
    image_binary.close()
    jsonData = {'type':'send','id':channel.id,'teams':teams,'sum':sum}
    return [imgDFile,json.dumps(jsonData)]


def obs(ctx, messages, mentions=[], author=None):
    tbl_mg, stbl_mg, track = search(messages,author)
    if tbl_mg == None:
        return {}
    tbl = table.fromMessage(tbl_mg)
    if mentions:
        users = set(map(lambda x:str(x).replace('#',''),mentions))
    else:
        users = {str(ctx.author).replace('#','')}
    users -= tbl.obs
    if not users:
        return {}
    tbl.obs |= users
    returnDict = {'embeds':[func.calObsEmbed(users=users),tbl.toEmbed()],'del':[tbl_mg]}
    if stbl_mg == None:
        return returnDict
    returnDict['embeds'].append(subTable.fromMessage(stbl_mg).toEmbed())
    returnDict['del'].append(stbl_mg)
    return returnDict

def upGSS(embed):
    if not isTable(embed):
        return
    tbl = table.fromEmbed(embed)
    if len(tbl.obs) == 0:
        return
    users = tbl.obs
    if tbl.form == 6:
        dif = tbl.sum[0] - tbl.sum[1]
        left = 12-int(tbl)
        win = int(dif > left*40)
        sokujiDict = {'teams':tbl.teams,'scores':tbl.sum,'left':left,'dif':'{:+}'.format(dif),'win':win}
        upDict = {}
        for user in users:
            upDict[user] = sokujiDict
        fbrtdb.update(upDict)
        return
    tblDict = dict(zip(tbl.teams,tbl.sum))
    tblDict_sorted = sorted(tblDict.items(), key=lambda x:x[1], reverse=True)
    teams = []
    scores = []
    for i in tblDict_sorted:
        teams.append(i[0])
        scores.append(i[1])
    sokujiDict = {'teams':teams,'scores':scores,'left':12-int(tbl)}
    upDict = {}
    for user in users:
        upDict[user] = sokujiDict
    fbrtdb.update(upDict)


if __name__ == '__main__':
    print(int(True))
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageChops
import json
import discord
import io
import os


ORIGINAL_COLOR = int(os.environ['COLOR'],0)

def mklog6(difs=[0]*12):
    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams['font.size'] = 20
    plt.rcParams['axes.facecolor'] = '#2c3e50'
    
    races = list(range(len(difs)+1))
    difs = [0] + difs
    difm = min(difs)
    difM = max(difs)
    if difm == 0:
        yList = [0, difM//2, difM]
    elif max(difs) == 0:
        yList = [difm, difm//2, 0]
    elif max([difM, -difm])//min([difM, -difm]) < 3:
        yList = [difm, 0, difM]
    else:
        yList = [difm, (difm+difM)/2, difM]

    plt.figure(facecolor='#2c3e50',figsize=(12.8,3))
    plt.xticks(range(0,len(races),3))
    plt.yticks(yList)
    plt.grid(axis='y', color='#95a5a6')
    plt.plot(races, [0]*len(races), color='#bdc3c7')
    plt.plot(races, difs, color='#c0392b',linewidth=4)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_linewidth(2)
    plt.gca().spines['bottom'].set_linewidth(2)
    plt.gca().spines['left'].set_color('#4F7090')
    plt.gca().spines['bottom'].set_color('#4F7090')
    plt.tick_params(axis='x', colors='#7f8c8d')
    plt.tick_params(axis='y', colors='#7f8c8d')
    plt.tick_params(color='#2c3e50')
    plt.tight_layout()
    img_binary = io.BytesIO()
    plt.savefig(img_binary, format='png')
    img_binary.seek(0)
    img = Image.open(img_binary)
    return img

def add_margin(pil_img, top=0, right=0, bottom=0, left=0, color='#2c3e50'):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def trimLR(img,color):
    bg = Image.new(mode="RGB", size=img.size, color=color)
    diff = ImageChops.difference(img, bg)
    croprange = diff.convert("RGB").getbbox()
    return img.crop((croprange[0],0,croprange[2],img.height))

def teamTxtImg6(team):
    boldLFont = ImageFont.truetype('fonts/NotoSansCJKjp-Bold.otf', size=250)
    img = Image.new(mode='RGB',size=(2000,300),color='#2c3e50')
    draw = ImageDraw.Draw(img)
    draw.text((0,125), team, fill='#3498db', font=boldLFont,anchor='lm')
    img = trimLR(img,'#2c3e50')
    if img.width > 500:
        img = img.resize((500,img.height))
    return img

def addTxt6(img, sum, teams):
    team1 = teams[0]
    team2 = teams[1]
    img = add_margin(img,top=420)
    firstImg = Image.open('png/first.png')
    secondImg = Image.open('png/second.png')
    boldLFont = ImageFont.truetype('fonts/NotoSansCJKjp-Bold.otf', size=250)
    boldSFont = ImageFont.truetype('fonts/NotoSansCJKjp-Bold.otf', size=100)
    thinFont = ImageFont.truetype('fonts/NotoSansCJKjp-Thin.otf', size=50)

    tema1TxtImg = teamTxtImg6(team1)
    img.paste(tema1TxtImg,(110,155))
    tema2TxtImg = teamTxtImg6(team2)
    img.paste(tema2TxtImg,(1170-tema2TxtImg.width,155))

    if sum[0] > sum[1]:
        rankImg1 = firstImg
        rankImg2 = secondImg
    elif sum[0] < sum[1]:
        rankImg1 = secondImg
        rankImg2 = firstImg
    else:
        rankImg1 = firstImg
        rankImg2 = firstImg
    img.paste(rankImg1,(120,40),rankImg1)
    img.paste(rankImg2,(1032,40),rankImg2)

    draw = ImageDraw.Draw(img)
    draw.text((640,50), f'{sum[0]} - {sum[1]}', fill='#3498db', font=boldSFont, anchor='ma')
    draw.text((640,85), '({:+})'.format(sum[0]-sum[1]), fill='#3498db', font=thinFont, anchor='mb')
    return img

def make6(difs, sum, teams):
    img = mklog6(difs)
    return addTxt6(img,sum,teams)

def toEmbed(message):
    global ORIGINAL_COLOR
    content = message.content
    jsonData = json.loads(content)
    embed = discord.Embed(title=' - '.join(jsonData['teams']),color=ORIGINAL_COLOR)
    embed.set_image(url=message.attachments[0].url)
    return embed

if __name__ == '__main__':
    make6([16,-6,-8,-10,-28,-8,-40,-32,-24,-42,-60,-50],[563,421],['BPBP','Gesjq']).save('tmp/tmp.png')
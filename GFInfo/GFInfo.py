import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False
import os
import re
import json
import requests


class GFInfo:
    """Return T-doll info from wiki"""

    def __init__(self, bot):
        self.bot = bot
        self.api_key = "3f6fc1942e5454a10b07dc1d9c70f5c1fa9850ff"
        self.output_type = "2"
        self.testmode = "0"
        self.db = "99"
        self.numres = "5"

    @commands.command(pass_context=True, no_pm=True)
    async def tcraftname(self, ctx, *, input):
        """Show gacha girl info by name"""
        cmd = "name"
        await self.search_command(ctx, cmd, input)


    @commands.command(pass_context=True, no_pm=True)
    async def tcrafttime(self, ctx, *, input):
        """Show gacha girl info by time"""
        cmd = "time"
        await self.search_command(ctx, cmd, input)
        

    async def search_command(self, ctx, cmd, input):
        path = "data/GF/Data.txt"
        found = False
        with open(path, "rb") as f:
            try:
                encoding = chardet.detect(f.read())["encoding"]
            except:
                encoding = "ISO-8859-1"
        with open(path, "r", encoding=encoding) as f:
            data_list = f.readlines()
        #Your code will go here
        for line in data_list:
            if cmd == "name":
                if input.lower() in line.lower():
                    found = True
                    await self.bot.say(line)
            if cmd == "time":
                if input in line.split():
                    found = True
                    await self.bot.say(line)
        if found == False:
            await self.bot.say("Result not found")
            
    @commands.command(pass_context=True, no_pm=True)
    async def tinfo(self, ctx, *, input):
        """Show girl info"""
        path = "data/GF/tdoll.txt"
        found = False
        with open(path, "rb") as f:
            try:
                encoding = chardet.detect(f.read())["encoding"]
            except:
                encoding = "ISO-8859-1"
        with open(path, "r", encoding=encoding) as f:
            data_list = f.readlines()
            for line in data_list:
                if input.lower() in line.lower():
                    found = True
                    await self.search_tdoll(ctx, line)
            if found == False:
                await self.bot.say("Can't find " + input)

    async def search_tdoll(self, ctx, input):
        path = "data/GF/tdoll.json"
        iconFolder = "data/GF/icon/"
        url = "https://en.gfwiki.com/wiki/"

        star2Url = "https://en.gfwiki.com/images/2/25/2Stars.png"
        star3Url = "https://en.gfwiki.com/images/d/dd/3Stars.png"
        star4Url = "https://en.gfwiki.com/images/4/41/4Stars.png"
        star5Url = "https://en.gfwiki.com/images/8/81/5Stars.png"
        extraStar = "https://en.gfwiki.com/images/3/38/EXTRAstar2.png"
        if ' ' in input:
            input = '_'.join(input.split());
        fullUrl = url+input
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        embed=discord.Embed(color = 13525284)
        if data[input.rstrip()]["rank"] == "2":
            iconPath = star2Url
        elif data[input.rstrip()]["rank"] == "3":
            iconPath = star3Url
        elif data[input.rstrip()]["rank"] == "4":
            iconPath = star4Url
        elif data[input.rstrip()]["rank"] == "5":
            iconPath = star5Url
        else:
            iconPath = extraStar
        embed.set_author(name=data[input.rstrip()]["name"], url=fullUrl, icon_url=iconPath)
        embed.set_thumbnail(url=data[input.rstrip()]["imageURL"])
        embed.add_field(name="Type", value=data[input.rstrip()]["type"], inline=True)
        embed.add_field(name="Pool", value=data[input.rstrip()]["pool"], inline=True)
        embed.add_field(name="Craft Time", value=data[input.rstrip()]["time"], inline=False)
        embed.add_field(name="Drop Map", value=data[input.rstrip()]["drop"], inline=True)
        embed.add_field(name="Reward", value=data[input.rstrip()]["reward"], inline=True)
        embed.add_field(name="Skills", value=data[input.rstrip()]["skill"]["name"] + " - " + data[input.rstrip()]["skill"]["effect"], inline=True)
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True, no_pm=True)
    async def sauce(self, ctx, input):
        """Show gacha girl info by name"""
        defaultLink = "https://saucenao.com/search.php?"
        fullLink = defaultLink + "db=" + self.db + "&output_type=" + self.output_type + "&testmode=" + self.testmode + "&numres=" + self.numres + "&api_key=" + self.api_key + "&url=" + input
        extension = [".jpg", ".png", ".gif", ".webp", ".svg",".tif", ".tiff" , ".jif", ".jfif", ".jp2", ".jpx", ".j2k", ".j2c", ".fpx", ".pcd"]
        for ex in extension:
            if ex in fullLink:
                i = fullLink.index(ex)
                fullLink = fullLink[:i+len(ex)]
        r = requests.get(fullLink)
        if r.status_code == 200:
            data = self.load_json(r)
            for result in data["results"]:
                embed=discord.Embed(title="Result")
                embed.add_field(name="Similarity", value=result["header"]["similarity"], inline=False)
                embed.add_field(name="Name", value=result["header"]["index_name"], inline=True)
                if 'eng_name' in result["data"]:
                    embed.add_field(name="Eng Name", value=result["data"]["eng_name"], inline=True)
                if 'jp_name' in result["data"]:
                    embed.add_field(name="JP Name", value=result["data"]["jp_name"], inline=True)
                if 'ext_urls' in result["data"]:
                    embed.add_field(name="Url", value=result["data"]["ext_urls"], inline=True)
                if 'danbooru_id' in result["data"]:
                    embed.add_field(name="Url", value=result["data"]["danbooru_id"], inline=True)
                if 'gelbooru_id' in result["data"]:
                    embed.add_field(name="Url", value=result["data"]["gelbooru_id"], inline=True)
                if 'pixiv_id' in result["data"]:
                    embed.add_field(name="Url", value=result["data"]["pixiv_id"], inline=True)
                if 'title' in result["data"]:
                    embed.add_field(name="Url", value=result["data"]["title"], inline=True)
                await self.bot.say(embed=embed)

    def load_json(self, result):
        try:
          data = json.loads(result.text)
          return data
        except ValueError:
          print("Url Error.") 

    @commands.command(pass_context=True)
    async def nyaa(self, ctx, input):
        """Find sukebei link"""
        defaultLink = "https://sukebei.nyaa.si/?f=0&c=1_3&q="
        fullLink = defaultLink + input
        #await self.bot.say(fullLink)
        result = requests.get(fullLink)
        soup = BeautifulSoup(result.content, 'html.parser')
        tableTorrent = soup.select('table tr')
        torrents = []
        for row in tableTorrent:
            block = []
            for td in row.find_all('td'):
                if td.find_all('a'):
                    for link in td.find_all('a'):
                        if link.get('href')[-9:] != '#comments':
                            block.append(link.get('href'))
                            if link.text.rstrip():
                                block.append(link.text)

                if td.text.rstrip():
                    block.append(td.text.rstrip())
            try:
                if len(block) == 11:
                    torrent = {
                        'url': "http://sukebei.nyaa.si{}".format(block[1]),
                        'name': block[2],
                        'size': block[6],
                        'date': block[7],
                        'seeders': block[8],
                        'leechers': block[9],
                        'completed_downloads': block[10],
                    }
                else:
                    torrent = {
                        'url': "http://sukebei.nyaa.si{}".format(block[1]),
                        'name': block[2],
                        'size': block[5],
                        'date': block[6],
                        'seeders': block[7],
                        'leechers': block[8],
                        'completed_downloads': block[9],
                    }
                torrents.append(torrent)
            except IndexError as ie:
                pass

        for link in torrents:
            embed=discord.Embed(title=link['name'], url=link['url'])
            embed.add_field(name="Size", value=link['size'], inline=True)
            embed.add_field(name="Date", value=link['date'], inline=True)
            embed.add_field(name="Completed Downloads", value=link['completed_downloads'], inline=False)
            embed.add_field(name="Seeder", value=link['seeders'], inline=True)
            embed.add_field(name="Leecher", value=link['leechers'], inline=True)
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def samefag(self, ctx, *, input):
        """You all are the same"""
        filename = "spiderman.jpg"
        fileafter = "after.jpg"
        path = "data/meme/"
        image = Image.open(path+filename)
        if os.path.exists(path + fileafter):
            os.remove(path + fileafter)
        if (ctx.message.mentions.__len__()>0 and ctx.message.mentions.__len__() <= 2):
            url = []
            for user in ctx.message.mentions:
                url.append(user.avatar_url)
            
            response1 = requests.get(url[0])
            img1 = Image.open(BytesIO(response1.content))
            width1, height1 = img1.size
            ratio1 = min(60/width1, 60/height1)
            newW1 = width1 * ratio1
            newH1 = height1 * ratio1
            img1.thumbnail((newW1, newH1))

            response2 = requests.get(url[1])
            img2 = Image.open(BytesIO(response2.content))
            width2, height2 = img2.size
            ratio2 = min(60/width2, 60/height2)
            newW2 = width2 * ratio2
            newH2 = height2 * ratio2
            img2.thumbnail((newW2, newH2))

            image = Image.open(path+filename)
            image.paste(img1, (197,66,257,126))
            image.paste(img2, (570,75,630,135))
            image.save(path + fileafter)
            await bot.send_file(path + fileafter)
        else:
            await self.bot.say("Mention 2 faggot only")
        
        

def setup(bot):
    if soupAvailable:
        bot.add_cog(GFInfo(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
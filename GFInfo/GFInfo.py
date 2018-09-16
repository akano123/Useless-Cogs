import discord
from discord.ext import commands

try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False
import aiohttp
import os
import re
import urllib.request
import json


class GFInfo:
    """Return T-doll info from wiki"""

    def __init__(self, bot):
        self.bot = bot

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
        with open(path) as f:
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

def setup(bot):
    if soupAvailable:
        bot.add_cog(GFInfo(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
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
            

def setup(bot):
    if soupAvailable:
        bot.add_cog(GFInfo(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
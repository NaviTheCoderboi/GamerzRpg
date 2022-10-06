import discord
from discord.ext import commands
import os
from db import *
from dotenv import load_dotenv

load_dotenv()

class botclass(commands.Bot):
    def __init__(self):
        self.exp = Exp()
        self.region = Region()
        self.stats = Stats()
        self.wallet = Wallet()
        self.items = Items()
        super().__init__(command_prefix="+",help_command=None,intents=discord.Intents.all())

    async def setup_hook(self):
        await self.exp.setup()
        await self.region.setup()
        await self.stats.setup()
        await self.wallet.setup()
        await self.items.setup()
        #print(await self.items.create(893363878728192041,"sword",1))
        print(await self.exp.update(893363878728192041,exp=210,level=1))
        print("Loading cogs . . .")
        cogs = []
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                cogs.append("cogs." + f[:-3])
        try:
            for cog in cogs:
                await bot.load_extension(cog)
                print(f"{cog} was loaded")
        except Exception as e:
            print(e)
        self.tree.copy_global_to(guild=discord.Object(id=1022409249428611073))
        await self.tree.sync()

bot = botclass()

bot.run(os.getenv("token"))

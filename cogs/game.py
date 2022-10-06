import discord
from discord.ext import commands
from discord import app_commands,Embed
from json import load,dumps
import random
import asyncio
from collections import Counter

class Shop(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="potions",emoji="<:potion_1:1023146682369703956>",description="potions category in shop!")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "potions":
            embed = Embed(title="shop - potions")
            embed.add_field(name="potions",value="**1**: <:potion_1:1023146682369703956> healing potion **id**: #01 **cost**: 30")
            embed.set_footer(text="use the /buy command to buy items")
            await interaction.response.edit_message(embed=embed)

class ShopView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Shop())

async def item_complete(interaction: discord.Interaction,current: str):
    ids = ["#01","#02"]
    return [
        app_commands.Choice(name=i,value=i)
        for i in ids if current.lower() in i.lower()
    ]

class game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.h = "<:health:1023160442031460442>"
        self.emo = {"healing potion": "<:potion_1:1023146682369703956>","sword": "<:atk:1023823345852104724>"}

    def entities(self,name):
        file = open(f"stats/entities/{name}.json")
        resp = load(file)
        return [resp["health"],resp["attack"]]

    def hp(self,id,cur):
        perc = cur/id*100
        if perc<=10:
            return f"{self.h}"
        elif perc<=20:
            return f"{self.h}{self.h}"
        elif perc<=30:
            return f"{self.h}{self.h}{self.h}"
        elif perc<=40:
            return f"{self.h}{self.h}{self.h}{self.h}"
        elif perc<=50:
            return f"{self.h}{self.h}{self.h}{self.h}{self.h}"
        elif perc<=60:
            return f"{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}"
        elif perc<=70:
            return f"{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}"
        elif perc<=80:
            return f"{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}"
        elif perc<=90:
            return f"{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}"
        elif perc<=100:
            return f"{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}{self.h}"

    async def check(self,user):
        user = await self.bot.exp.read(user)
        if user != False:
            return True
        else:
            return False

    @app_commands.command(name="buy",description="buy an item from the shop!")
    @app_commands.describe(item="id of the item to buy")
    @app_commands.autocomplete(item=item_complete)
    async def _buy(self,interaction: discord.Interaction, item: str):
        user = interaction.user
        checking = await self.check(user.id)
        if checking == False:
            await interaction.response.send_message("Ah! The user has not started the game yet.\nFor what are you waiting! suggest him/her now.")
        else:
            wal = await self.bot.wallet.read(interaction.user.id)
            if item == "#01":
                if wal.money >= 30:
                    itemcheck = await self.bot.items.read(interaction.user.id,"healing potion")
                    if itemcheck:
                        let = itemcheck.quantity+1
                        await self.bot.items.updatequantity(interaction.user.id,"healing potion",let)
                    else:
                        await self.bot.items.create(interaction.user.id,"healing potion")
                    await interaction.response.send_message(embed=Embed(title=interaction.user, description=f"successfully buyed {self.emo.get('healing potion')}healing potion!"))
                else:
                    await interaction.response.send_message(embed=Embed(title=interaction.user, description="you don't have enough money to buy it!"))
            else:
                await interaction.response.send_message(embed=Embed(title=interaction.user, description="This item is not available yet!"))

    @app_commands.command(name="shop",description="view the shop!")
    async def _shop(self,interaction: discord.Interaction):
        embed = Embed(
            title="shop",
            description="choose the shop category from drop-down below!"
        )
        embed.set_footer(text="use the /buy command to buy items")
        await interaction.response.send_message(embed=embed,view=ShopView())

    @app_commands.command(name="ping", description="replies with pong!")
    async def _ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("pong!")

    @app_commands.command(name="inventory", description="view your inventory!")
    async def _inventory(self, interaction: discord.Interaction):
        user = interaction.user
        checking = await self.check(user.id)
        if checking == False:
            await interaction.response.send_message("Ah! The user has not started the game yet.\nFor what are you waiting! suggest him/her now.")
        else:
            all_items = await self.bot.items.readall(user.id)
            if all_items == False:
                embed = Embed(title=f"{user}'s inventory",description="no item in your inventory")
            else:
                items = all_items.item
                embed = Embed(
                    title=f"{user}'s inventory",
                    description="•••••••••••••••••••\n"
                )
                for i in items:
                    embed.description += f"• {self.emo.get(i[1])}**{i[1]}** - {i[2]}x\n** **\n"
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="wallet", description="view a user's wallet!")
    @app_commands.describe(user="the user whose wallet to view")
    async def _wallet(self, interaction: discord.Interaction, user: discord.Member = None):
        if user == None:
            user = interaction.user
        checking = await self.check(user.id)
        if checking == False:
            await interaction.response.send_message("Ah! The user has not started the game yet.\nFor what are you waiting! suggest him/her now.")
        else:
            wallet = await self.bot.wallet.read(interaction.user.id)
            embed = Embed(
                title=user,
                description=f"💵**money**: {wallet.money}\n💰**vote money**: {wallet.vmoney}\n*vote for our bot on https://top.gg to earn vote coins!*"
            )
            embed.set_thumbnail(url=user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="profile", description="view a user's profile!")
    @app_commands.describe(user="the user whose profile to view")
    async def _profile(self, interaction: discord.Interaction, user: discord.Member = None):
        if user == None:
            user = interaction.user
        checking = await self.check(user.id)
        if checking == False:
            await interaction.response.send_message("Ah! The user has not started the game yet.\nFor what are you waiting! suggest him/her now.")
        else:
            region = await self.bot.region.read(interaction.user.id)
            wallet = await self.bot.wallet.read(interaction.user.id)
            level = await self.bot.exp.read(interaction.user.id)
            stats = await self.bot.stats.read(interaction.user.id)
            embed = Embed(
                title=user,
                description=f"**region**: {region.region}\n**wallet**: {wallet.money}\n**vote money**: {wallet.vmoney}\n**level**: {level.level}\n**exp**: {level.exp}"
            )
            embed.add_field(name="stats",value=f"<:health:1023160442031460442>**health**: {stats.hp}\n:shield:**defence**: {stats.defence}\n<:atk:1023823345852104724>**attack**: {stats.atk}")
            embed.set_thumbnail(url=user.avatar.url)
            embed.set_image(url="https://media.discordapp.net/attachments/1022779620648566826/1023813738635198474/standard.gif")
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="start", description="start your adventure!")
    async def _start(self, interaction: discord.Interaction):
        user = await self.bot.exp.read(interaction.user.id)
        if user != False:
            await interaction.response.send_message("You have already started the game!")
        else:
            newuser = await self.bot.exp.create(interaction.user.id)
            region = await self.bot.region.create(interaction.user.id)
            wallet = await self.bot.wallet.create(interaction.user.id)
            stats = await self.bot.stats.create(interaction.user.id)
            items = await self.bot.items.create(interaction.user.id,"healing potion",1)
            new_embed = Embed(
                title=interaction.user,
                description="Welcome to Gamerz Rpg!",
                color=discord.Color.green()
            )
            new_embed.set_image(url="https://media.discordapp.net/attachments/1022779620648566826/1022779667880620103/standard.gif")
            new_embed.add_field(name="Ah good!",value=f"+200 💵\n+1 healing potion <:potion_1:1023146682369703956>")
            new_embed.add_field(name="exp",value=f"```\n{newuser.exp}```")
            new_embed.add_field(name="level",value=f"```\n{newuser.level}```")
            new_embed.add_field(name="region",value=f"```\n{region.region}```")
            await interaction.response.send_message(embed=new_embed)

    @app_commands.command(name="wild", description="start a wild battle!")
    async def _wild(self, inter: discord.Interaction):
        user = await self.check(inter.user.id)
        if user == False:
            await inter.response.send_message("Ah! you have not started the game.\nPlease start by using `/start` command.")
        else:
            region = await self.bot.region.read(inter.user.id)
            if region.region == 1:
                ran = random.randint(1,5)
                if ran<=3:
                    entity = "mouse"
                elif ran == 4:
                    entity = "gyarados"
                elif ran == 5:
                    entity = "heatran"
                user_stats = await self.bot.stats.read(inter.user.id)
                opposite_stats = self.entities(entity)
                user_curhp = user_stats.hp
                opposite_curhp = opposite_stats[0]
                embed1 = Embed(
                    title=inter.user,
                    description=f"**You**: {self.hp(user_stats.hp,user_stats.hp)}\n```{user_curhp}/{user_stats.hp}```\n**{entity}**: {self.hp(opposite_stats[0],opposite_stats[0])}\n```{opposite_curhp}/{opposite_stats[0]}```"
               )
                file = discord.File(f"sprites/{entity}.jpg",filename=f"{entity}.jpg")
                embed1.set_image(url=f"attachment://{entity}.jpg")
                embed1.set_footer(text="Type `1` to attack,`2` to defend or `3` to use potions")
                await inter.response.send_message(file=file,embed=embed1)
                alive = True
                def mss(msg):
                    return msg.author.id == inter.user.id and msg.channel == inter.channel
                while alive == True:
                    mes = await self.bot.wait_for('message',check=mss)
                    if mes.content == '1':
                        user_dmg = random.randint(user_stats.atk,user_stats.atk+2)
                        opposite_curhp = opposite_curhp-user_dmg
                        opposite_dmg = random.randint(opposite_stats[1],opposite_stats[1]+2)
                        user_curhp = user_curhp-opposite_dmg
                        if opposite_curhp<1:
                            cur_exp = await self.bot.exp.read(inter.user.id)
                            await self.bot.exp.update(inter.user.id,cur_exp.exp+5)
                            embed = Embed(title=inter.user, description=f"{entity} fainted,You have won the battle!\n`+5` Exp:sparkles:\n```current exp: {cur_exp.exp+5}```")
                            await inter.channel.send(embed=embed)
                            alive = False
                            exp = await self.bot.exp.read(inter.user.id)
                            stats = await self.bot.stats.read(inter.user.id)
                            if exp.exp >= 100 * (exp.level + 1):
                                if exp.level == 0:
                                    new_exp = exp.exp-100
                                else:
                                    a = 1+exp.level
                                    c = a*100
                                    b = exp.exp
                                    new_exp = b-c
                                new_hp = stats.hp+random.randint(1,2)
                                new_atk = stats.atk+random.randint(1,2)
                                new_def = stats.defence+random.randint(1,2)
                                await self.bot.stats.update(inter.user.id,new_hp,new_def,new_atk)
                                await self.bot.stats.read(inter.user.id)
                                new_level = exp.level+1
                                await self.bot.exp.update(id=inter.user.id,level=new_level,exp=new_exp)
                                new = await self.bot.exp.read(inter.user.id)
                                embed = Embed(title=inter.user, description=f"congratulations! you have level up to level {new.level}!\n```exp: {new.exp}\nlevel: {new.level}```")
                                await inter.channel.send(embed=embed)
                        elif user_curhp<1:
                            embed = Embed(title=inter.user,description=f"You fainted,{entity} won the battle")
                            await inter.channel.send(embed=embed)
                            alive = False
                        else:
                            embed = Embed(title=inter.user, description=f"You use attack,{entity} lost `{user_dmg}` hp!\n{entity} used attack.\nyou lost`{opposite_dmg}` hp")
                            await inter.channel.send(embed=embed)
                            await asyncio.sleep(1.5)
                            embed1 = Embed(
                                title=inter.user,
                                description=f"**You**: {self.hp(user_stats.hp,user_curhp)}\n```{user_curhp}/{user_stats.hp}```\n**{entity}**: {self.hp(opposite_stats[0],opposite_curhp)}\n```{opposite_curhp}/{opposite_stats[0]}```"
                            )
                            file = discord.File(f"sprites/{entity}.jpg",filename=f"{entity}.jpg")
                            embed1.set_image(url=f"attachment://{entity}.jpg")
                            embed1.set_footer(text="Type `1` to attack,`2` to defend or `3` to use potions")
                            await inter.channel.send(file=file,embed=embed1)
                    elif mes.content == '2':
                        user_defence = user_stats.defence
                        if random.randint(1,3)<3:
                            healed = random.randint(user_defence-1,user_defence)
                            if user_curhp >29:
                                healed = 0
                            else:
                                healed=healed
                            if user_curhp > 30:
                                user_curhp = 30
                                healed = 0
                            user_curhp = user_curhp+healed
                            defend = True
                        else:
                            opposite_dmg = random.randint(opposite_stats[1],opposite_stats[1]+2)
                            user_curhp = user_curhp-opposite_dmg
                            defend = False
                        if opposite_curhp<1:
                            cur_exp = await self.bot.exp.read(inter.user.id)
                            await self.bot.exp.update(inter.user.id,cur_exp.exp+5)
                            embed = Embed(title=inter.user, description=f"{entity} fainted,You have won the battle!\n`+5` Exp:sparkles:\n```current exp: {cur_exp.exp+5}```")
                            await inter.channel.send(embed=embed)
                            alive = False
                        elif user_curhp<1:
                            embed = Embed(title=inter.user,description=f"You fainted,{entity} won the battle")
                            await inter.channel.send(embed=embed)
                            alive = False
                        else:
                            if defend == True:
                                embed = Embed(title=inter.user, description=f"You used defend.\nYou healed {healed}hp")
                            else:
                                embed = Embed(title=inter.user, description=f"You used defend.\nYou were not able to defend!")
                            await inter.channel.send(embed=embed)
                            await asyncio.sleep(1)
                            embed1 = Embed(
                                title=inter.user,
                                description=f"**You**: {self.hp(user_stats.hp,user_curhp)}\n```{user_curhp}/{user_stats.hp}```\n**{entity}**: {self.hp(opposite_stats[0], opposite_curhp)}\n```{opposite_curhp}/{opposite_stats[0]}```"
                            )
                            file = discord.File(f"sprites/{entity}.jpg",filename=f"{entity}.jpg")
                            embed1.set_image(url=f"attachment://{entity}.jpg")
                            embed1.set_footer(text="Type `1` to attack,`2` to defend or `3` to use potions")
                            await inter.channel.send(file=file,embed=embed1)
                    elif mes.content == '3':
                        item = await self.bot.items.read(inter.user.id,"healing potion")
                        if item == False:
                            quantity = 0
                        else:
                            quantity = item.quantity
                        embed = Embed(title=inter.user,description=f"**1** - {self.emo.get('healing potion')}**healing potion**: {quantity}")
                        await inter.channel.send(embed=embed)
                        mes = mes = await self.bot.wait_for('message',check=mss)
                        if mes.content == "1":
                            if quantity>0:
                                if user_curhp>=user_stats.hp:
                                    embed = Embed(title=inter.user, description="Your hp is already full! you cannot use potion")
                                    await inter.channel.send(embed=embed)
                                    await asyncio.sleep(1)
                                    embed1 = Embed(
                                        title=inter.user,
                                        description=f"**You**: {self.hp(user_stats.hp,user_curhp)}\n```{user_curhp}/{user_stats.hp}```\n**{entity}**: {self.hp(opposite_stats[0], opposite_curhp)}\n```{opposite_curhp}/{opposite_stats[0]}```"
                                    )
                                    file = discord.File(f"sprites/{entity}.jpg",filename=f"{entity}.jpg")
                                    embed1.set_image(url=f"attachment://{entity}.jpg")
                                    embed1.set_footer(text="Type `1` to attack,`2` to defend or `3` to use potions")
                                    await inter.channel.send(file=file,embed=embed1)
                                else:
                                    user_curhp = user_curhp+5
                                    if user_curhp>user_stats.hp:
                                        user_curhp=user_stats.hp
                                    c = await self.bot.items.updatequantity(inter.user.id,"healing potion",quantity-1)
                                    if quantity-1==0:
                                        await self.bot.items.delete(inter.user.id,"healing potion")
                                    embed = Embed(title=inter.user, description="you used potion! you healed 5hp!")
                                    await inter.channel.send(embed=embed)
                                    await asyncio.sleep(1)
                                    embed1 = Embed(
                                        title=inter.user,
                                        description=f"**You**: {self.hp(user_stats.hp,user_curhp)}\n```{user_curhp}/{user_stats.hp}```\n**{entity}**: {self.hp(opposite_stats[0], opposite_curhp)}\n```{opposite_curhp}/{opposite_stats[0]}```"
                                    )
                                    file = discord.File(f"sprites/{entity}.jpg",filename=f"{entity}.jpg")
                                    embed1.set_image(url=f"attachment://{entity}.jpg")
                                    embed1.set_footer(text="Type `1` to attack,`2` to defend or `3` to use potions")
                                    await inter.channel.send(file=file,embed=embed1)
                            else:
                                embed = Embed(title=inter.user, description="you don't have healing potion!\nPlease buy it from shop to use it.")
                                await inter.channel.send(embed=embed)
                                await asyncio.sleep(1)
                                embed1 = Embed(
                                    title=inter.user,
                                    description=f"**You**: {self.hp(user_stats.hp,user_curhp)}\n```{user_curhp}/{user_stats.hp}```\n**{entity}**: {self.hp(opposite_stats[0], opposite_curhp)}\n```{opposite_curhp}/{opposite_stats[0]}```"
                                )
                                file = discord.File(f"sprites/{entity}.jpg",filename=f"{entity}.jpg")
                                embed1.set_image(url=f"attachment://{entity}.jpg")
                                embed1.set_footer(text="Type `1` to attack,`2` to defend or `3` to use potions")
                                await inter.channel.send(file=file,embed=embed1)

async def setup(bot):
    await bot.add_cog(game(bot))
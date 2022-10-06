from __future__ import annotations
import aiosqlite
from collections import namedtuple

class Wallet:
    async def setup(self):
        self.conn = await aiosqlite.connect("dbs/wallet.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute('''
        CREATE TABLE IF NOT EXISTS wallet(id INTEGER,money INTEGER,vmoney INTEGER)
            ''')
        await self.conn.commit()
        self.named_tuple = namedtuple("user", ["id", "money", "vmoney",])

    async def read(self,id: int):
        _data = await self.cur.execute("SELECT * FROM wallet WHERE id = ?", (id,))
        data = await _data.fetchone()
        if not data:
            return False
        else:
            return self.named_tuple(data[0],data[1],data[2])
    
    async def create(self,id: int,money:int =200,vmoney:int =0):
        _check = await self.read(id)
        if _check:
            return True
        else:
            await self.cur.execute("INSERT INTO wallet(id, money,vmoney) VALUES(?,?,?)", (id,money,vmoney))
            await self.conn.commit()
            return self.named_tuple(id,money,vmoney)

    async def update(self,id: int,money: int=None,vmoney:int = None):
        if not money:
            return False
        elif money and not vmoney:
            await self.cur.execute("UPDATE wallet SET money = ? WHERE id = ?",(money,id))
            await self.conn.commit()
            return True
        elif vmoney and not money:
            await self.cur.execute("UPDATE wallet SET vmoney = ? WHERE id = ?",(vmoney,id))
            await self.conn.commit()
            return True
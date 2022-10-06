from __future__ import annotations
import aiosqlite
from collections import namedtuple
from .exp import Exp

class Items:
    async def setup(self):
        self.conn = await aiosqlite.connect("dbs/items.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute('''
        CREATE TABLE IF NOT EXISTS items(id INTEGER,item STRING,quantity INTEGER)
            ''')
        await self.conn.commit()
        self.named_tuple = namedtuple("user", ["item","quantity",])
        self.named_tuple1 = namedtuple("user",["item",])

    async def read(self,id: int,item: str):
        _data = await self.cur.execute("SELECT * FROM items WHERE id = ? AND item = ?", (id,item,))
        data = await _data.fetchone()
        if not data:
            return False
        else:
            return self.named_tuple(data[1],data[2])

    async def readall(self,id: int):
        _data = await self.cur.execute("SELECT * FROM items WHERE id = ?", (id,))
        data = await _data.fetchall()
        if not data:
            return False
        else:
            return self.named_tuple1(data)

    async def create(self,id: int,item: str, quantity=1):
        await self.cur.execute("INSERT INTO items(id, item, quantity) VALUES(?, ?, ?)", (id,item,quantity,))
        await self.conn.commit()
        return self.named_tuple(item, quantity)

    async def update(self,id: int,old_item: str,new_item: str):
        if not new_item and old_item:
            return False
        else:
            await self.cur.execute("UPDATE items SET item = ? WHERE item = ? AND id = ?", (new_item,old_item,id))
            await self.conn.commit()
            return True

    async def updatequantity(self,id: int,item: str, quantity: int):
        if not id:
            return False
        else:
            await self.cur.execute("UPDATE items SET quantity = ? WHERE item = ? AND id = ?", (quantity,item,id))
            await self.conn.commit()
            return True

    async def delete(self,id: int,item: str):
        if not item:
            return False
        else:
            await self.cur.execute("DELETE FROM items WHERE id = ? AND item = ?",(id,item))
            await self.conn.commit()
            return True
from __future__ import annotations
import aiosqlite
from collections import namedtuple

class Region:
    async def setup(self):
        self.conn = await aiosqlite.connect("dbs/region.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute('''
        CREATE TABLE IF NOT EXISTS region(id INTEGER,region INTEGER)
            ''')
        await self.conn.commit()
        self.named_tuple = namedtuple("user", ["id", "region",])

    async def read(self,id: int):
        _data = await self.cur.execute("SELECT * FROM region WHERE id = ?", (id,))
        data = await _data.fetchone()
        if not data:
            return False
        else:
            return self.named_tuple(data[0],data[1])
    
    async def create(self,id: int,region=1):
        _check = await self.read(id)
        if _check:
            return True
        else:
            await self.cur.execute("INSERT INTO region(id, region) VALUES(?, ?)", (id, region))
            await self.conn.commit()
            return self.named_tuple(id,region)

    async def update(self,id: int,region):
        if not exp and level:
            return False
        elif region:
            await self.cur.execute("UPDATE region SET region = ? WHERE id = ?", (region, id,))
            await self.conn.commit()
            return True
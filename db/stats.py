from __future__ import annotations
import aiosqlite
from collections import namedtuple

class Stats:
    async def setup(self):
        self.conn = await aiosqlite.connect("dbs/stats.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute('''
        CREATE TABLE IF NOT EXISTS stats(id INTEGER,hp INTEGER,defence INTEGER,atk INTEGER)
            ''')
        await self.conn.commit()
        self.named_tuple = namedtuple("user", ["id","hp", "defence","atk",])

    async def read(self,id: int):
        _data = await self.cur.execute("SELECT * FROM stats WHERE id = ?", (id,))
        data = await _data.fetchone()
        if not data:
            return False
        else:
            return self.named_tuple(data[0],data[1],data[2],data[3])
    
    async def create(self,id: int,hp=30,atk=5,defence=1):
        _check = await self.read(id)
        if _check:
            return True
        else:
            await self.cur.execute("INSERT INTO stats(id, hp,defence,atk) VALUES(?, ?,?,?)", (id, hp,defence,atk))
            await self.conn.commit()
            return self.named_tuple(id,hp,defence,atk)

    async def update(self,id: int,hp: int=None,defence: int=None,atk: int=None):
        if not id:
            return False
        else:
            await self.cur.execute("UPDATE stats SET hp = ? WHERE id = ?", (hp, id,))
            await self.cur.execute("UPDATE stats SET defence = ? WHERE id = ?", (defence, id,))
            await self.cur.execute("UPDATE stats SET atk = ? WHERE id = ?", (atk, id,))
            await self.conn.commit()
            return True
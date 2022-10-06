from __future__ import annotations
import aiosqlite
from collections import namedtuple

class Exp:
    async def setup(self):
        self.conn = await aiosqlite.connect("dbs/exp.db")
        self.cur = await self.conn.cursor()
        await self.cur.execute('''
        CREATE TABLE IF NOT EXISTS exp(id INTEGER,exp INTEGER,level INTEGER)
            ''')
        await self.conn.commit()
        self.named_tuple = namedtuple("user", ["id", "exp", "level",])

    async def read(self,id: int):
        _data = await self.cur.execute("SELECT * FROM exp WHERE id = ?", (id,))
        data = await _data.fetchone()
        if not data:
            return False
        else:
            return self.named_tuple(data[0],data[1],data[2])
    
    async def create(self,id: int,level = 0,exp=20):
        _check = await self.read(id)
        if _check:
            return True
        else:
            await self.cur.execute("INSERT INTO exp(id, exp, level) VALUES(?, ?, ?)", (id, exp, level))
            await self.conn.commit()
            return self.named_tuple(id,exp,level)

    async def update(self,id: int,exp=None,level=None):
        if not exp and level:
            return False
        elif level and not exp:
            await self.cur.execute("UPDATE exp SET level = ? WHERE id = ?", (level, id,))
            await self.conn.commit()
            return True
        elif exp and not level:
            await self.cur.execute("UPDATE exp SET exp = ? WHERE id = ?", (exp, id,))
            await self.conn.commit()
            return True
        elif exp and level:
            await self.cur.execute("UPDATE exp SET exp = ? WHERE id = ?", (exp, id,))
            await self.cur.execute("UPDATE exp SET level = ? WHERE id = ?", (level, id,))
            await self.conn.commit()
            return True
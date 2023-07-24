import sqlalchemy as sa
import datetime

from sqlalchemy import Column, String, BigInteger

from data import create_bot

from gino import Gino
from typing import List
from aiogram import Dispatcher

from data.create_bot import POSTGRES_URI

db: Gino = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"
    

class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now())


    
async def on_startup(dispatcher: Dispatcher):
    print('Установка связи с Postgresql')
    await db.set_bind(create_bot.POSTGRES_URI)

async def on_shutdown(dispatcher: Dispatcher):
    await db.pop_bind().close()
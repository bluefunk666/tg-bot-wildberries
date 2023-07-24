from aiogram import Bot, Dispatcher, types
#from aioredis import Redis

from data import create_bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from misc.db_api.db_gino import db


bot = Bot(token=create_bot.TOKEN, parse_mode=types.ParseMode.HTML)

#redis = Redis()
#redis.

storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'db']
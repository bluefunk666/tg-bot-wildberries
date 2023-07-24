#from aiogram import Bot, Dispatcher
#from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
#from misc.db_api.db_gino import db
import os

#import bot

load_dotenv()
TOKEN = str(os.getenv("BOT_TOKEN"))


ip = os.getenv('ip')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"


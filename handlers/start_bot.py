import logging
import os
import time
from aiogram import types, Dispatcher
from loader import bot, dp
from keyboards import kb_client
from aiogram.dispatcher.filters import Text
from misc.throttling import rate_limit
from dotenv import load_dotenv
from misc.db_api import quick_commands as commands


@rate_limit(limit=3)
@dp.message_handler(text='/start')
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    await message.answer(f'Привет {user_full_name}\n'
                         f'Это бот для доставки Ваших заказов с маркетплейсов России. \nПожалуйста, для корректной работы бота используйте меню ', reply_markup=kb_client)



import logging
import time
from aiogram import types, Dispatcher
from loader import bot
from keyboards import kb_client
from aiogram.dispatcher.filters import Text
from misc.throttling import rate_limit

#@dp.message_handler(commands=['start'])
#@rate_limit(limit=3)
#async def start_handler(message: types.Message):
#    user_id = message.from_user.id
 #   user_full_name = message.from_user.full_name
#    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    
 #   await message.reply(f"Привет, {user_full_name}, это бот для доставки Ваших заказов с маркетплейсов России. \nПожалуйста, для корректной работы бота используйте меню ", reply_markup=kb_client)

#@dp.message_handler(commands=['help'])\
@rate_limit(limit=3)
async def help_handler(message: types.Message):
        await bot.send_message(message.from_user.id, "По техническим вопросам можете обращаться к *****")
@rate_limit(limit=3)
async def faq_handler(message: types.Message):
    await bot.send_message(message.from_user.id, "Для того, чтобы оформить заказ, Вам нужно прислать скриншот необходимого товара, а также артикул и количество нужного Вам товара.\n"
                                                 "Важно: Для того чтобы заказать сразу несколько товаров, Вы заполняете данные для каждого товара единожды, после каждого товара, в случае надобности, вы оформляете данные по следующему товару. Если в процессе заказа вы передумали, вы можете отменить сбор информации командой \"отмена\"")



@rate_limit(limit=3)
def register_handlers_client(dp : Dispatcher ):
#    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(help_handler, lambda message: 'Помощь' in message.text)
    dp.register_message_handler(help_handler, Text(equals='помощь', ignore_case=True))
    dp.register_message_handler(faq_handler, lambda message: 'Как пользоваться' in message.text)
    dp.register_message_handler(faq_handler, Text(equals='как пользоваться', ignore_case=True))

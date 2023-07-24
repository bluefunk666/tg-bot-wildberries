from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher, executor
from loader import bot
from aiogram.dispatcher.filters import Text
from misc.throttling import rate_limit
from misc.db_api import quick_commands as commands
from misc.db_api.schemas.user import User
from keyboards.client_kb import otmena, start_re, menu_but, kb_client, zakaz_da_net
from keyboards.admin_kb import admin_panel
from bs4 import BeautifulSoup
import logging
import time
import os
import aiohttp
from aiogram.utils import markdown as md
import html
import datetime
from dotenv import load_dotenv


class FSMuser(StatesGroup):
    photo = State()
    article = State()
    price = State()
    amount = State()

ADMIN_ID = os.getenv('ADMIN_ID')


@rate_limit(limit=3)
async def add_new_order(message):
    order = await quick_commands.get_last_order()
    
    
    await send_admin_notification(order)
    
    
@rate_limit(limit=3)
async def send_admin_notification(order):
  text = f"Новый заказ No{order.id} от {order.username} на сумму {order.total_price} руб"
  
  await bot.send_message(ADMIN_ID, text)




@rate_limit(limit=3)
async def admin(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы авторизовались как админ', reply_markup=admin_panel)
    else:
        await message.answer('Я не знаю такой команды')


@rate_limit(limit=3)
async def count_users(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        count = await commands.count_users()
        await message.answer(count)
    else:
        await message.answer('Я не знаю такой команды')

@rate_limit(limit=3)
async def count_users_24hrs(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        chat_id = message.from_user.id
        orders = await commands.count_users_last_24h()
        for order in orders:
            caption = ""
            caption += f"<b>ID Пользователя:</b> {order.user_id}\n"
            caption += f"<b>Артикул:</b> <code>{order.article}</code>\n"
            caption += f"<b>Цена:</b> {order.price}\n"
            caption += f"<b>Количество:</b> {order.amount}\n\n"
            if order.username:
                caption += f"<b>Имя пользователя:</b> @{order.username}\n"
            else:
                chat = await bot.get_chat(order.user_id)
                caption += f"<b>Имя пользователя:</b> <a href='tg://user?id={chat.id}'>{chat.first_name}</a>\n"
        
            caption += f"<b>Дата заказа:</b> {order.created_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
            await bot.send_photo(chat_id=chat_id, photo=order.photo, caption=caption, parse_mode='HTML')
    else:
        await message.answer('Я не знаю такой команды')
    
    

@rate_limit(limit=3)
async def cm_start(message : types.Message):
    await FSMuser.photo.set()
    await message.reply('📷 Загрузите скриншот необходимого товара\n❗️ Важно: для каждого товара Вы заполняете данные только 1 раз', reply_markup=otmena)


async def all_users(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
         chat_id = message.from_user.id
         users = await commands.all_users()
         for user in users:
             caption = ""
             caption += f"<b>ID Пользователя:</b> {user.user_id}\n"
             caption += f"<b>Артикул:</b> <code>{user.article}</code>\n"
             caption += f"<b>Цена:</b> {user.price}\n"
             caption += f"<b>Количество:</b> {user.amount}\n\n"
             if user.username:
                caption += f"<b>Имя пользователя:</b> @{user.username}\n"
             else:
                chat = await bot.get_chat(user.user_id)
                caption += f"<b>Имя пользователя:</b> <a href='tg://user?id={chat.id}'>{chat.first_name}</a>\n"
             caption += f"<b>Дата заказа:</b> {user.created_at.strftime('%d-%m-%Y %H:%M:%S')}\n"
             await bot.send_photo(chat_id=chat_id, photo=user.photo, caption=caption, parse_mode='HTML')
    else:
        await message.answer('Я не знаю такой команды')


@rate_limit(limit=3)
async def vse_zakazi(message: types.Message):
    user_id = message.from_user.id
    users = await commands.get_user_data_last_30min(user_id)
    result = []
    for user in users:
        result.append(user.price * user.amount)
    total = sum(result) * 1.1
    await message.reply(f"Итоговая цена ваших товаров, учитывая доставку составляет: {total:.2f} рублей.\nОжидайте обратной связи", reply_markup=menu_but)


async def not_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    if message.text == '❌Отмена':
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
        await bot.send_message(message.from_user.id, 'Вы отменили заказ и перешли в главное меню', reply_markup=kb_client)
    elif message.text == '🆘 Помощь':
        await bot.send_message(message.from_user.id,
                               f"{user_full_name}, если вам потребуется помощь, или Вам непонятен функционал бота, "
                               f"вы можете обращаться к Максиму Александровичу - @Maxim_MironovDNR", reply_markup=menu_but)
        await state.finish()
    elif message.text == '🔙 Меню':
        await bot.send_message(message.from_user.id, f'{user_full_name}, Выберите действие',
                               reply_markup=kb_client)
        await state.finish()
    else:
        await message.answer('Это не фотография')

@rate_limit(limit=3)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMuser.next()
    await message.reply('🔢 Теперь введите артикул данного товара', reply_markup=otmena)


@rate_limit(limit=3)
async def load_article(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    if message.text == '❌Отмена':
        await bot.send_message(message.from_user.id, 'Вы отменили заказ и перешли в главное меню', reply_markup=kb_client)
        await state.finish()
    elif message.text == '🆘 Помощь':
        await bot.send_message(message.from_user.id,
                         f"{user_full_name}, если вам потребуется помощь, или Вам непонятен функционал бота "
                         f"Вы можете обращаться к Максиму Александровичу - @Maxim_MironovDNR", reply_markup=menu_but)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['article'] = message.text

        await FSMuser.next()
        await message.reply('Теперь введите цену данного товара 💵 (Цифрами)', reply_markup=otmena)


@rate_limit(limit=3)
async def load_price(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    if message.text.isdigit():
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await bot.send_message(message.from_user.id, "❓ В каком количестве?", reply_markup=otmena)
        await FSMuser.next()
    elif message.text == '❌Отмена':
        await bot.send_message(message.from_user.id, 'Вы отменили заказ и перешли в главное меню', reply_markup=kb_client)
        await state.finish()
    elif message.text == '🆘 Помощь':
        await bot.send_message(message.from_user.id,
                         f"{user_full_name}, если вам потребуется помощь, или Вам непонятен функционал бота "
                         f"Вы можете обращаться к Максиму Александровичу - @Maxim_MironovDNR", reply_markup=menu_but)
        await state.finish()

    else:
        await message.reply('Введите цифры')
        if message.text.isdigit():
            async with state.proxy() as data:
                data['price'] = int(message.text)
            await bot.send_message(message.from_user.id, "❓ В каком количестве?", reply_markup=otmena)
            await FSMuser.next()

    
@rate_limit(limit=3)
async def amount(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['amount'] = int(message.text)
        async with state.proxy() as data:
            combined_data = f"Photo: {data['photo']}, Article: {data['article']}, Price: {data['price']}, Amount: {data['amount']}"
            values = combined_data.split(", ")
            user_id = message.from_user.id
            username = message.from_user.username
            photo, article, price, amount = [value.split(": ")[1] for value in values]
            await commands.create_table(user_id=user_id, username=username, photo=photo, article=article,
                                        price=int(price), amount=int(amount))
            itog = round(data['price'] * data['amount'] * 1.1)
            await message.reply(f"✔️ Ваш заказ принят в обработку.\nХотите заказать еще один товар? ", reply_markup=zakaz_da_net)

            await state.finish()
    else:
        await message.reply('Введите количество необходимого вам товара в цифрах')
        if message.text.isdigit():
            async with state.proxy() as data:
                data['amount'] = int(message.text)
            async with state.proxy() as data:
                combined_data = f"Photo: {data['photo']}, Article: {data['article']}, Price: {data['price']}, Amount: {data['amount']}"
                values = combined_data.split(", ")
                user_id = message.from_user.first_name
                username = message.from_user.full_name
                photo, article, price, amount = [value.split(": ")[1] for value in values]
                await commands.create_table(user_id=user_id, username=username, photo=photo, article=article,
                                             price=int(price), amount=int(amount))
                itog = round(data['price'] * data['amount'] * 1.1)
                await message.reply(f"✔️ Хорошо, итоговая стоимость данного товара, учитывая доставку = {itog}. \nХотите заказать еще один товар?", reply_markup=zakaz_da_net)


                await state.finish()


@rate_limit(limit=3)
async def help(message:types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    await bot.send_message(message.from_user.id, f"{user_full_name}, если вам потребуется помощь, или Вам непонятен функционал бота"
                                                 f"Вы можете обращаться к Максиму Александровичу - @Maxim_MironovDNR", reply_markup=menu_but)

@rate_limit(limit=3)
async def after_order(message:types.message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    await bot.send_message(message.from_user.id, f'{user_full_name}, Вы перешли в главное меню', reply_markup=kb_client)

    


@rate_limit(limit=3)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Вы перешли в главное меню', reply_markup=kb_client)



    
def register_handlers_fsmuser(dp : Dispatcher ):
    dp.register_message_handler(cm_start, lambda message: 'Начать' in message.text, state = None)
    dp.register_message_handler(cm_start, Text(equals='начать', ignore_case=True), state=None)
    dp.register_message_handler(cm_start, Text(equals='Да, я хочу заказать еще один товар', ignore_case=True), state=None)
    dp.register_message_handler(not_photo, lambda message: not message.photo, state=FSMuser.photo)
    dp.register_message_handler(load_photo, content_types =['photo'], state=FSMuser.photo)
    dp.register_message_handler(load_article, state = FSMuser.article)
    dp.register_message_handler(load_price, state = FSMuser.price)
    dp.register_message_handler(amount, state=FSMuser.amount)
    dp.register_message_handler(help, lambda message: 'Помощь' in message.text, state ='*')
    dp.register_message_handler(help, Text(equals='Помощь', ignore_case=True), state='*')
    dp.register_message_handler(vse_zakazi, Text(equals='Нет, я уже заказал все товары', ignore_case=True))
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(after_order, lambda message: 'Меню' in message.text)
    dp.register_message_handler(after_order, Text(equals='меню', ignore_case=True), state="*")
    dp.register_message_handler(admin, Text(equals='админ', ignore_case=True), state="*")
    dp.register_message_handler(count_users, lambda message: "Общее количество заказов" in message.text)
    dp.register_message_handler(all_users, lambda message: "Заказы за все время" in message.text)
    dp.register_message_handler(count_users_24hrs, lambda message: "Заказы за сегодня" in message.text)
    dp.register_message_handler(add_new_order, lambda message: message.text.lower() == 'Нет, я уже заказал все товары') 
    dp.register_message_handler(send_admin_notification, lambda message: message.text.lower() == 'Нет, я уже заказал все товары')
    

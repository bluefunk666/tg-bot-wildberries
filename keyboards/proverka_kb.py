from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

yess = KeyboardButton('Да')
No = KeyboardButton('Нет')

prov_client = ReplyKeyboardMarkup(resize_keyboard=True)
prov_client.add(yess).add(No)
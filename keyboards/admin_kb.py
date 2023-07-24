from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Общее количество заказов').add('Заказы за сегодня').add('Заказы за все время')
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('🛠 Как пользоваться')
b2 = KeyboardButton('🆘 Помощь')
b3 = KeyboardButton('✅ Начать')
b4 = KeyboardButton('Отмена')

menu = KeyboardButton('🔙 Меню')
menu_but = ReplyKeyboardMarkup(resize_keyboard=True)
menu_but.add(menu)

zakaz_da_net = ReplyKeyboardMarkup(resize_keyboard=True)
da = KeyboardButton('Да, я хочу заказать еще один товар')
net = KeyboardButton('Нет, я уже заказал все товары')
zakaz_da_net.add(da).add(net)



kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

restart = KeyboardButton('✅ Начать')
start_re = ReplyKeyboardMarkup(resize_keyboard=True)
start_re.add(start_re).add(b2)
otmena = ReplyKeyboardMarkup(resize_keyboard=True)

otmena.add(b2).add("❌Отмена")

kb_client.add(b3).add(b2).insert(b1)

from aiogram import executor
from handlers import client, admin, start_bot
from loader import bot, dp
#from misc.db_api.db_gino import db

async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    from misc.db_api.db_gino import on_startup, db
    print('Подключение к Postgresql')
    await on_startup(dp)

    #print('Удаление базы данных')
    #await db.gino.drop_all()

    print('Создание таблиц')
    await db.gino.create_all()

    print('Готово')


client.register_handlers_client(dp) 
#other.register_handlers_other(dp)
admin.register_handlers_fsmuser(dp)

if __name__ == '__main__':
    #import middlewares
    #middlewares.setup(dp)
    executor.start_polling(dp, on_startup=on_startup)



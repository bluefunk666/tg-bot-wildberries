from datetime import datetime, timedelta
from aiogram.types import Update
from asyncpg import UniqueViolationError
from loader import bot
#from misc.db_api.db_gino import db

from misc.db_api.schemas.user import User
from misc.db_api.db_gino import db


async def create_table(user_id: int, username: str, photo: str, article: str, price: int, amount: int):
    user = User(user_id=user_id,
                #id_tg=id_tg,
                username=username,
                photo=photo,
                article=article,
                price=price,
                amount=amount)
    await user.create()



async def select_all_users():
    users = await User.query.gino.all()
    return users


async def all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def handle_command(update: Update, context):
    chat_id = update.message.chat_id
    users = await all_users()
    message = ""
    for user in users:
        message += f"User ID: {user.user_id}\n"
        message += f"Username: {user.username}\n"
        message += f"Photo: {user.photo}\n"
        message += f"Article: {user.article}\n"
        message += f"Price: {user.price}\n"
        message += f"Amount: {user.amount}\n\n"
    await bot.send_message(chat_id=chat_id, text=message)


async def get_user_data_last_30min(user_id):
    start_time = datetime.now() - timedelta(minutes=30)
    user_data = await User.query.where(
        (User.user_id == user_id) & (User.created_at > start_time)
    ).gino.all()
    return user_data

async def get_last_order():
    order = await User.query.order_by(User.id.desc()).gino.first()
    return order


async def count_users_last_24h():
    start_time = datetime.now() - timedelta(hours=48)
    orders = await User.query.where(User.created_at > start_time).gino.all()
    return orders

async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def update_user_name(user_id, new_name):
    user = await select_user(user_id)
    await user.update(update_name=new_name).apply()

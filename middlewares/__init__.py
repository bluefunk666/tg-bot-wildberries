from aiogram import Dispatcher
from middlewares import throttling
from .throttling import ThrottlingMiddleware



def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
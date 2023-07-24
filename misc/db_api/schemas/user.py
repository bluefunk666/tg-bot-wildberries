from misc.db_api.db_gino import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql
from datetime import datetime


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger)
    username = Column(String(70))
    #id_tg = Column(String(200))
    photo = Column(String(300))
    article = Column(String(100))
    price = Column(BigInteger)
    #choice = Column(String(50))
    amount = Column(BigInteger)


    query: sql.select
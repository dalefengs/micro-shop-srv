from abc import ABC

from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


# 使用 peewee 的连接池， 使用ReconnectMixin 来防止出现连接断开查询失败
class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase, ABC):
    pass


MYSQL_DB = "shop_user_srv"
MYSQL_HOST = "172.17.0.1"
MYSQL_USERNAME = "root"
MYSQL_PASSWD = "000"
MYSQL_PORT = 3306

DB = ReconnectMysqlDatabase(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USERNAME,
                            password=MYSQL_PASSWD)

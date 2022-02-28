import nacos
import json
from abc import ABC
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


# 使用 peewee 的连接池， 使用ReconnectMixin 来防止出现连接断开查询失败
class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase, ABC):
    pass


def update_cfg(args):
    print("配置发生了变化")
    global config
    config = json.dumps(args)
    print(config)


NACOS = {
    "host": "172.17.0.1",
    "port": 8848,
    "user": "nacos",
    "password": "000",
    "name_space": "19c7769b-a69b-40e0-ac4c-d9e43307e5b6",  # 命名空间
    "group": "dev",
    "user_srv_data_id": "goods-srv",
    "db_data_id": "db",
}

nacos_client = nacos.NacosClient(f'{NACOS["host"]}:{NACOS["port"]}', namespace=NACOS["name_space"])
# nacos 返回的是字符串，需要使用json.loads加载
# 默认配置0
config = json.loads(nacos_client.get_config(NACOS["user_srv_data_id"], NACOS["group"]))

# 数据库配置
db = json.loads(nacos_client.get_config(NACOS["db_data_id"], NACOS["group"]))
mysql = db["mysql"]

DB = ReconnectMysqlDatabase(mysql["db"], host=mysql["host"], port=mysql["port"], user=mysql["username"],
                            password=mysql["password"])

# 监听配置文件修改  PS：如果是Window系统可能会出现错误，需要在 main方法中调用
nacos_client.add_config_watcher(NACOS["user_srv_data_id"], NACOS["group"], update_cfg)
nacos_client.add_config_watcher(NACOS["db_data_id"], NACOS["group"], update_cfg)

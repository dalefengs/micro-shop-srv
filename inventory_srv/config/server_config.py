import redis
from inventory_srv.config.config import config

consul = config["consul"]
redisConfig = config["redis"]

HOST = config["host"]
SERVER_NAME = config["server_name"]
SERVER_TAGS = config["server_tags"]
# Consul 配置
CONSUL_HOST = consul["host"]
CONSUL_PORT = consul["port"]

# Redis 配置
REDIS_HOST = redisConfig["host"]
REDIS_PORT = redisConfig["port"]
REDIS_DB = redisConfig["db"]
REDIS_PREFIX = redisConfig["prefix"]  # 后缀

# Redis 连接池

redisPool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
redisStrict = redis.StrictRedis(connection_pool=redisPool)

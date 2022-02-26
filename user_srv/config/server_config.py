from user_srv.config.config import config

consul = config["consul"]
HOST = config["host"]
PORT = config['port']
SERVER_NAME = config["server_name"]
SERVER_TAGS = config["server_tags"]
# Consul 配置
CONSUL_HOST = consul["host"]
CONSUL_PORT = consul["port"]

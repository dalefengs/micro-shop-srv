import argparse
import logging
import os
import signal
import sys
import socket
import grpc
from concurrent import futures
from loguru import logger
from functools import partial


# 因为在终端上运行会找不到根目录所以需要指明项目根目录
BASE_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, BASE_PATH)

from inventory_srv.proto import inventory_pb2,inventory_pb2_grpc
from inventory_srv.handler.inventory import InventoryServicer
from inventory_srv.config import server_config

from common.grpc_health.v1 import health_pb2_grpc
from common.grpc_health.v1 import health
from common.register.consul import ConsulRegister


def on_exit(signal, frame, service_id):
    logger.info("服务注消中...")
    c = ConsulRegister(host=server_config.CONSUL_HOST, port=server_config.CONSUL_PORT)
    if not c.deregister(service_id=service_id):
        logger.error("服务注销失败")
    logger.info(f"{server_config.SERVER_NAME}服务已注销")
    sys.exit(0)


# 动态获取可用的端口号
def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',
                        nargs="?",
                        type=str,
                        default=server_config.HOST,
                        help="binding ip"
                        )
    parser.add_argument('--port',
                        nargs="?",
                        type=int,
                        default=get_free_tcp_port(),  # 动态获取
                        help="the listening port"
                        )
    args = parser.parse_args()

    logger.add("logs/user_srv_{time}.log")
    # 多线程启动
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 注册服务
    inventory_pb2_grpc.add_InventoryServicer_to_server(InventoryServicer(), server)
    # 注册健康检查
    health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    # 端口
    # server.add_insecure_port("[::]:50051")
    server.add_insecure_port(f'{args.ip}:{args.port}')
    import uuid
    service_id = str(uuid.uuid1())
    # 监听退出信号
    """
        windows下支持的信号是有限的：
            SIGINT ctrl+C终端
            SIGTERM kill发出的软件终止
    因为 on_exit 前两个参数是自动注入的，所以需要使用partial重新包装一下
    """
    signal.signal(signal.SIGINT, partial(on_exit,service_id=service_id))
    signal.signal(signal.SIGTERM, partial(on_exit,service_id=service_id))

    logger.info(f"启动服务: {args.ip}:{args.port}!")
    server.start()

    logger.info("服务注册中...")
    c = ConsulRegister(host=server_config.CONSUL_HOST, port=server_config.CONSUL_PORT)
    success = c.register(name=server_config.SERVER_NAME, service_id=service_id, address=args.ip,
                         port=args.port, tags=server_config.SERVER_TAGS, check=None)
    if not success:
        logger.error("服务注册失败!")
        sys.exit(0)
    logger.info(f"{server_config.SERVER_NAME}服务注册成功!")

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

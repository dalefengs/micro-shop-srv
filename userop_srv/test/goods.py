import grpc
import consul
from userop_srv.proto import order_pb2, order_pb2_grpc
from userop_srv.config import server_config


class OrderTest:
    def __init__(self):
        # 连接 Consul
        c = consul.Consul("172.17.0.1", 8500)
        services = c.agent.services().items()
        ip = ""
        port = 0
        for k, v, in services:
            if v["Service"] == server_config.SERVER_NAME:
                ip = v["Address"]
                port = v["Port"]
                break

        # 连接 grpc 服务器
        channel = grpc.insecure_channel(f"{ip}:{port}")
        self.order_stub = order_pb2_grpc.OrderStub(channel)

    def order_list(self):
        rsp: order_pb2.OrderListResponse = self.order_stub.OrderList(
            order_pb2.OrderFilterRequest(keyWords="越南")
        )
        for item in rsp.data:
            print(item)
            print(item.name, item.shopPrice)


if __name__ == "__main__":
    t = OrderTest()
    t.order_list()

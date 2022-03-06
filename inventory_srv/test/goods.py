import grpc
import consul
from inventory_srv.proto import goods_pb2, goods_pb2_grpc
from inventory_srv.config import server_config


class GoodsTest:
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
        self.goods_stub = goods_pb2_grpc.GoodsStub(channel)

    def goods_list(self):
        rsp: goods_pb2.GoodsListResponse = self.goods_stub.GoodsList(
            goods_pb2.GoodsFilterRequest(keyWords="越南")
        )
        for item in rsp.data:
            print(item)
            print(item.name, item.shopPrice)


if __name__ == "__main__":
    t = GoodsTest()
    t.goods_list()

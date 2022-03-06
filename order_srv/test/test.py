import grpc
import consul
from order_srv.proto import order_pb2, order_pb2_grpc
from order_srv.config import server_config, config


class Test:
    def __init__(self):
        # 连接 Consul
        c = consul.Consul(server_config.CONSUL_HOST, server_config.CONSUL_PORT)
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

    def CreateCart(self):
        rsp = self.order_stub.CreateCartItem(order_pb2.CartItemRequest(userId=1, goodsId=421, nums=3, checked=True))
        rsp = self.order_stub.CreateCartItem(order_pb2.CartItemRequest(userId=1, goodsId=422, nums=1, checked=False))
        rsp = self.order_stub.CreateCartItem(order_pb2.CartItemRequest(userId=1, goodsId=422, nums=1, checked=False))
        print(rsp)

    def CartItemList(self):
        rsp = self.order_stub.CartItemList(order_pb2.UserInfo(id=1))
        print(rsp)

    def UpdateCartItem(self):
        rsp = self.order_stub.UpdateCartItem(order_pb2.CartItemRequest(userId=1, goodsId=421, checked=True))
        print(rsp)

    def DeleteCartItem(self):
        rsp = self.order_stub.DeleteCartItem(order_pb2.CartItemRequest(id=4))
        print(rsp)

    def CreateOrder(self):
        o_r = order_pb2.OrderRequest(userId=1, address="地址", mobile="18166669999", name="冯", post="留言")
        rsp = self.order_stub.CreateOrder(o_r)
        print(rsp)

    def OrderList(self):
        rsp = self.order_stub.OrderList(order_pb2.OrderFilterRequest(userId=1))
        print(rsp)

    def OrderDetail(self):
        rsp = self.order_stub.OrderDetail(order_pb2.OrderRequest(id=8))
        print(rsp)

    def UpdateOrderStatus(self):
        rsp = self.order_stub.UpdateOrderStatus(order_pb2.OrderStatus(OrderSn="20220306154538175", status="TRADE_SUCCESS"))
        print(rsp)


if __name__ == '__main__':
    test = Test()
    # test.CreateCart()
    # test.CartItemList()
    # test.DeleteCartItem()
    # test.CreateOrder()
    # test.OrderList()
    # test.OrderDetail()
    test.UpdateOrderStatus()

import time

import grpc
from loguru import logger
from peewee import DoesNotExist
from google.protobuf import empty_pb2
from order_srv.model.models import ShoppingCart, OrderInfo, OrderGoods

from order_srv.proto import order_pb2, order_pb2_grpc
from order_srv.proto import goods_pb2, goods_pb2_grpc
from order_srv.proto import inventory_pb2, inventory_pb2_grpc
from common.register import consul
from order_srv.config import config, server_config


# 生成订单号
def generate_order_sn(user_id):
    from random import Random
    order_sn = f'{time.strftime("%Y%m%d%H%M%S")}{user_id}{Random().randint(10, 99)}'
    return order_sn


class OrderService(order_pb2_grpc.OrderServicer):
    @logger.catch
    def CartItemList(self, request: order_pb2.UserInfo, context):
        rsp = order_pb2.CartItemListResponse()
        users = ShoppingCart.select().where(ShoppingCart.user == request.id)
        if not list:
            return rsp
        rsp.total = users.count()
        for item in users:
            data = order_pb2.ShopCartInfoResponse()
            data.id = item.id
            data.userId = item.user
            data.goodsId = item.goods
            data.nums = item.nums
            data.checked = item.checked
            rsp.data.append(data)
        return rsp

    # 添加购物车
    @logger.catch
    def CreateCartItem(self, request: order_pb2.CartItemRequest, context):
        rsp = order_pb2.ShopCartInfoResponse()
        # 如果商品添加过则增加数量
        try:
            car = ShoppingCart.get(ShoppingCart.user == request.userId, ShoppingCart.goods == request.goodsId)
            car.nums += request.nums
        except DoesNotExist:
            car = ShoppingCart()
            car.goods = request.goodsId
            car.user = request.userId
            car.nums = request.nums
            car.checked = False
        car.save()
        rsp.id = car.id
        rsp.goodsId = request.goodsId
        rsp.userId = request.userId
        rsp.nums = request.nums
        rsp.checked = False
        return rsp

    @logger.catch
    def UpdateCartItem(self, request, context):
        # 更新购物车条目-数量和选中状态
        try:
            item = ShoppingCart.get(ShoppingCart.user == request.userId, ShoppingCart.goods == request.goodsId)
            item.checked = request.checked
            if request.nums:
                item.nums = request.nums
            item.save()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("购物车记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    def DeleteCartItem(self, request, context):
        # 删除购物车条目
        try:
            item = ShoppingCart.get(ShoppingCart.user == request.userId, ShoppingCart.goods == request.goodsId)
            item.delete_instance()
            return empty_pb2.Empty()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("购物车记录不存在")
            return empty_pb2.Empty()

    # 更新购物车选中状态和数量
    @logger.catch
    def UpdateOrderStatus(self, request: order_pb2.CartItemRequest, context):
        try:
            cat = ShoppingCart.get(ShoppingCart.id == request.id)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_detail("记录不存在")
            return empty_pb2.Empty()

        if request.nums:
            cat.num = request.nums
        cat.checked = request.checked
        result = cat.sava()
        if not result:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_detail("添加购物车失败")
            return empty_pb2.Empty()
        return empty_pb2.Empty()

    @logger.catch
    def DeleteCartItem(self, request: order_pb2.CartItemRequest, context):
        try:
            cat = ShoppingCart.get(ShoppingCart.id == request.id)
            cat.delete_instance(permanently=True)
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_detail("记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    def CreateOrder(self, request: order_pb2.OrderRequest, context):
        rsp = order_pb2.OrderInfoResponse()

        # 获取购物车中被选中的商品和数量
        cat = ShoppingCart.select().where(ShoppingCart.user == request.userId, ShoppingCart.checked == True)
        goods_ids = []
        goods_nums = {}
        order_goods_list = []
        inv_rps = inventory_pb2.SellInfo()
        amount = 0
        # 访问商品服务获取商品价格
        for item in cat:
            goods_ids.append(item.goods)
            goods_nums[item.goods] = item.nums

        register = consul.ConsulRegister(host=server_config.CONSUL_HOST, port=server_config.CONSUL_PORT)
        goods_srv_host, goods_srv_port = register.get_host_port(server_config.GOODS_SRV_NAME)
        if not goods_srv_host:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("商品服务不可用")
            return rsp

        goods_channel = grpc.insecure_channel(f"{goods_srv_host}:{goods_srv_port}")
        goods_stud = goods_pb2_grpc.GoodsStub(goods_channel)
        try:
            goods_list = goods_stud.BatchGetGoods(goods_pb2.BatchGoodsIdInfo(id=goods_ids))
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"商品服务不可用:{str(e)}")
            return rsp
        for item in goods_list.data:
            amount += item.shopPrice * goods_nums[item.id]
            og = OrderGoods()
            og.goods = item.id
            og.name = item.name
            og.goods_image = item.goodsFrontImage
            og.goods_price = item.shopPrice
            og.nums = goods_nums[item.id]
            order_goods_list.append(og)
            # 组装库存信息
            inv_rps.goodsInfo.append(inventory_pb2.GoodsInvInfo(goodsId=item.id, num=goods_nums[item.id]))

        # 扣减库存

        inventory_srv_host, inventory_srv_port = register.get_host_port(server_config.INVENTORY_SRV_NAME)
        if not inventory_srv_host:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("库存服务不可用")
            return rsp

        inventory_channel = grpc.insecure_channel(f"{inventory_srv_host}:{inventory_srv_port}")
        inventory_stud = inventory_pb2_grpc.InventoryStub(inventory_channel)
        try:
            inventory_stud.Sell(inv_rps)
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"库存服务不可用:{str(e)}")
            return rsp

        with config.DB.atomic() as tnx:
            try:
                order = OrderInfo()
                order.order_sn = generate_order_sn(request.userId)
                order.order_mount = amount
                order.user = request.userId
                order.address = request.address
                order.singer_mobile = request.mobile
                order.signer_name = request.name
                order.post = request.post
                order.save()

                # 创建订单详情
                for og in order_goods_list:
                    og.order = order.id
                # 批量删除
                OrderGoods.bulk_create(order_goods_list)

                # 删除购物车中的商品
                ShoppingCart.delete(permanently=True).where(ShoppingCart.user == request.userId, ShoppingCart.checked == True)
            except Exception as e:
                tnx.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_detail("创建订单失败")
                return rsp

        rsp.id = order.id
        rsp.orderSn = order.order_sn
        rsp.total = order.order_mount
        return rsp

    @logger.catch
    def OrderList(self, request: order_pb2.OrderFilterRequest, context):
        rsp = order_pb2.OrderListResponse()
        offset = 0
        page = 1
        limit = 10
        if request.pages:
            page = request.pages

        if request.pagePerNums:
            limit = request.pagePerNums
            offset = (page - 1) * limit

        orders = OrderInfo.select()
        if request.userId:
            orders = orders.where(OrderInfo.user == request.userId)
        rsp.total = orders.count()
        orders = orders.limit(limit).offset(offset)
        for item in orders:
            data = order_pb2.OrderInfoResponse()
            data.id = item.id
            data.userId = item.user
            data.orderSn = item.order_sn
            data.payType = item.pay_type
            data.status = item.status
            data.post = item.post
            data.address = item.address
            data.name = item.signer_name
            data.mobile = item.singer_mobile
            rsp.data.append(data)

        return rsp

    @logger.catch
    def OrderDetail(self, request: order_pb2.OrderRequest, context):
        # 订单详情
        rsp = order_pb2.OrderInfoDetailResponse()
        try:
            if request.userId:
                order = OrderInfo.get(OrderInfo.id == request.id, OrderInfo.user == request.userId)
            else:
                order = OrderInfo.get(OrderInfo.id == request.id)

            rsp.orderInfo.id = order.id
            rsp.orderInfo.userId = order.user
            rsp.orderInfo.orderSn = order.order_sn
            rsp.orderInfo.payType = order.pay_type
            rsp.orderInfo.status = order.status
            rsp.orderInfo.post = order.post
            rsp.orderInfo.total = order.order_mount
            rsp.orderInfo.address = order.address
            rsp.orderInfo.name = order.signer_name
            rsp.orderInfo.mobile = order.singer_mobile

            order_goods = OrderGoods.select().where(OrderGoods.order == order.id)
            for order_good in order_goods:
                order_goods_rsp = order_pb2.OrderItemResponse()

                order_goods_rsp.goodsId = order_good.goods
                order_goods_rsp.goodsName = order_good.goods_name
                order_goods_rsp.goodsImage = order_good.goods_image
                order_goods_rsp.goodsPrice = float(order_good.goods_price)
                order_goods_rsp.nums = order_good.nums

                rsp.data.append(order_goods_rsp)

            return rsp
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("订单记录不存在")
            return rsp

    @logger.catch
    def UpdateOrderStatus(self, request, context):
        # 更新订单的支付状态 特别注意update语句需要调用 execute 方法才会执行
        OrderInfo.update(status=request.status).where(OrderInfo.order_sn == request.OrderSn).execute()
        return empty_pb2.Empty()

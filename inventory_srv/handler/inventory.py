import json

import grpc
import redis
from loguru import logger
from peewee import DoesNotExist
from google.protobuf import empty_pb2

from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from inventory_srv.model.models import Inventory
from inventory_srv.config import config, server_config
from common.redis_lock import redis_lock


class InventoryServicer(inventory_pb2_grpc.InventoryServicer):
    @logger.catch
    def GetInv(self, request: inventory_pb2.GoodsInvInfo, context):
        try:
            inv = Inventory.get(Inventory.goods == request.goodsId)
            return inventory_pb2.GoodsInvInfo(goodsId=inv.goods, num=inv.stocks)
        except DoesNotExist:
            context.set_code(404)
            context.set_details("记录不存在")
            return inventory_pb2.GoodsInvInfo()

    @logger.catch
    def SetInv(self, request: inventory_pb2.GoodsInvInfo, context):
        invs = Inventory.select().where(Inventory.goods == request.goodsId)
        if not invs:
            inv = Inventory()
            inv.goods = request.goodsId
        else:
            inv = invs[0]
        inv.goods = request.goodsId
        inv.stocks = request.num
        inv.save(force_insert=True)
        return empty_pb2.Empty()

    # 扣减库存
    @logger.catch
    def Sell(self, request: inventory_pb2.SellInfo, context):
        try:
            with config.DB.atomic() as txn:  # 开启事物
                for item in request.goodsInfo:
                    key = server_config.REDIS_PREFIX["inventory"] + "inventory_" + str(item.goodsId)
                    lock = redis_lock.Lock(server_config.redisStrict, key, auto_renewal=True, expire=10)
                    lock.acquire()
                    inv = Inventory.get(Inventory.goods == item.goodsId)
                    if inv.stocks < item.num:
                        context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
                        context.set_details(f"商品{item.goodsId},库存不足")
                        txn.rollback()  # 事物回滚
                        return empty_pb2.Empty()
                    inv.stocks -= item.num
                    inv.save()
                    lock.release()
                return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return empty_pb2.Empty()

    @logger.catch
    def Reback(self, request: inventory_pb2.SellInfo, context):
        try:
            with config.DB.atomic() as txn:  # 开启事物
                for item in request.goodsInfo:
                    key = server_config["prefix"]["inventory"] + "inventory_" + item.goodsId
                    lock = redis_lock.Lock(server_config.redisStrict, key, auto_renewal=True, expire=10)
                    lock.acquire()
                    inv = Inventory.get(Inventory.goods == item.goodsId)
                    inv.stocks -= item.num
                    inv.save()
                    lock.release()
                return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return empty_pb2.Empty()

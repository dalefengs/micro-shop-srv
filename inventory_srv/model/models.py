import threading
from datetime import datetime

from peewee import *
from inventory_srv.config import config, server_config
import redis


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_deleted = BooleanField(default=False, null=True, verbose_name="是否删除")
    update_time = DateTimeField(verbose_name="更新时间", default=datetime.now)

    def save(self, *args, **kwargs):
        if self._pk is None:
            self.create_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        return super(BaseModel, self).save(*args, **kwargs)

    @classmethod
    def delete(cls, permanently=False):
        if permanently:
            return super(BaseModel, cls).delete()
        else:
            return super(BaseModel, cls).update(is_deleted=True)

    @classmethod
    def select(cls, *selection):
        # 在大多数情况下,此方法有效,但在某些情况下,如果使用带有关键字“ IN”的联接结束结果查询时出现错误,则选择它会中断：“ 1241,’操作数应包含1列”
        return super(BaseModel, cls).select(cls, *selection).where(cls.is_deleted == False)

    def delete_instance(self, permanently=False, recursive=False, delete_nullable=False):
        if permanently:
            return self.delete(permanently).where(self.pk_expr()).execute()
        else:
            self.is_deleted = True
            return self.save()

    class Meta:
        database = config.DB


class Inventory(BaseModel):
    # 商品的库存表
    # stock = PrimaryKeyField(Stock)
    goods = IntegerField(verbose_name="商品id", unique=True)
    stocks = IntegerField(verbose_name="库存数量", default=0)
    version = IntegerField(verbose_name="版本号", default=0)  # 分布式锁的乐观锁


class InventoryNew(BaseModel):
    # 商品的库存表
    # stock = PrimaryKeyField(Stock)
    goods = IntegerField(verbose_name="商品id", unique=True)
    stocks = IntegerField(verbose_name="库存数量", default=0)
    version = IntegerField(verbose_name="版本号", default=0)  # 分布式锁的乐观锁
    freeze = IntegerField(verbose_name="冻结数量", default=0)


# class Delivery(BaseModel):
#     goods = IntegerField(verbose_name="商品id", unique=True)
#     goods_name = CharField(verbose_name="商品名")
#     nums = IntegerField(verbose_name="数量", unique=True)
#     order_sn = CharField(verbose_name="订单号")
#     status = CharField(verbose_name="订单号", default="waitting")

class InventoryHistory(BaseModel):
    # 出库历史表
    order_sn = CharField(verbose_name="订单编号", max_length=20, unique=True)
    order_inv_detail = CharField(verbose_name="订单详情", max_length=200)
    status = IntegerField(choices=((1, "已扣减"), (2, "已归还")), default=1, verbose_name="出库状态")


class RedisLock:
    def __init__(self, key, uuid=None):
        if uuid is None:
            import uuid
            uuid = uuid.uuid4()
        self.id = uuid
        self.redis_client = redis.Redis(host=server_config.REDIS_HOST, port=server_config.REDIS_PORT)
        self.key = f"{server_config.REDIS_PREFIX['inventory']}{key}"

    def acquire(self):

        while True:
            # if not self.redis_client.get(self.key):  # 错误的示范，高并发时可能出现同时进入代码的情况，不能保证原子性
            #     self.redis_client.set(self.key, 1)
            #     break
            # 获取到锁
            # 使用 setnx 获取不到时插入数据，保证数据的原子性
            # if self.redis_client.setnx(self.key, 1):  # 如果 key 存在返回False，不存在设置 key 并返回 True
            if self.redis_client.set(self.key, self.id, nx=True, ex=15):

                # 启动一个线程去定时刷新过期时间 最好也使用lua脚本完成 - 看门狗
                break
            else:  # 获取不到锁， 等待一秒重新获取
                import time
                time.sleep(1)

    def release(self):
        # 防止自己的锁被别人删除
        # 这里的存在文件，需要将代码原子化 redis 没有提供这样的接口，我们可以使用 lua 脚本让redis原子化执行
        id = self.redis_client.get(self.key)
        print(f"释放{self.key}")
        if id is not self.id:
            print("不能删除不属于自己的出锁")
            return
        self.redis_client.delete(self.key)


def sell():
    # 多线程下的并发带来的数据不一致的问题
    goods_list = [(1, 10), (2, 20), (3, 30)]
    with config.DB.atomic() as txn:
        # 超卖
        for goods_id, num in goods_list:
            lock = RedisLock(key=goods_id)
            # 查询库存 如果更新失败增重复尝试
            goods_inv = Inventory.get(Inventory.id == goods_id)
            print(f"商品{goods_id} 售出 {num}件")
            import time
            from random import randint

            time.sleep(randint(1, 2))
            if goods_inv.stocks < num:
                print(f"商品：{goods_id} 库存不足")
                txn.rollback()
                break
            else:
                # 获取锁
                lock.acquire()
                # 让数据库根据自己当前的值更新数据， 这个语句能不能处理并发的问题
                query = Inventory.update(stocks=Inventory.stocks - num).where(Inventory.id == goods_id)
                ok = query.execute()
                if ok:
                    print(f"商品：{goods_id} 更新成功")
                else:
                    print(f"商品：{goods_id} 更新失败")
                # 释放锁
                lock.release()


if __name__ == "__main__":
    config.DB.create_tables([Inventory, InventoryHistory])

    t1 = threading.Thread(target=sell)
    t2 = threading.Thread(target=sell)
    t3 = threading.Thread(target=sell)
    t4 = threading.Thread(target=sell)
    t5 = threading.Thread(target=sell)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

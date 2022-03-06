from peewee import *

from datetime import datetime

from peewee import *

from order_srv.config import config


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_deleted = BooleanField(default=False, verbose_name="是否删除")
    update_time = DateTimeField(verbose_name="更新时间", default=datetime.now)

    def save(self, *args, **kwargs):
        # 判断这是一个新添加的数据还是更新的数据
        if self._pk is not None:
            # 这是一个新数据
            self.update_time = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def delete(cls, permanently=False):  # permanently表示是否永久删除
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(self, permanently=False, recursive=False, delete_nullable=False):
        if permanently:
            return self.delete(permanently).where(self._pk_expr()).execute()
        else:
            self.is_deleted = True
            self.save()

    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(cls.is_deleted == False)

    class Meta:
        database = config.DB


class ShoppingCart(BaseModel):
    """
    购物车
    """
    user = IntegerField(verbose_name="用户id")
    goods = IntegerField(verbose_name="商品id")
    nums = IntegerField(verbose_name="购买数量")
    checked = BooleanField(default=True, verbose_name="是否选中")


class OrderInfo(BaseModel):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
    )

    PAY_TYPE = (
        ("alipay", "支付宝"),
    )

    user = IntegerField(verbose_name="用户id")
    order_sn = CharField(max_length=30, null=True, unique=True, verbose_name="订单号")
    pay_type = CharField(choices=PAY_TYPE, default="alipay", max_length=30, verbose_name="支付方式")
    status = CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="订单状态")
    trade_no = CharField(max_length=100, unique=True, null=True, verbose_name=u"交易号")
    order_mount = FloatField(default=0.0, verbose_name="订单金额")
    pay_time = DateTimeField(null=True, verbose_name="支付时间")

    # 用户信息
    address = CharField(max_length=100, default="", verbose_name="收货地址")
    signer_name = CharField(max_length=20, default="", verbose_name="签收人")
    singer_mobile = CharField(max_length=11, verbose_name="联系电话")
    post = CharField(max_length=20, default="", verbose_name="留言")


class OrderGoods(BaseModel):
    """
    订单的商品详情
    """
    order = IntegerField(verbose_name="订单id")
    goods = IntegerField(verbose_name="商品id")
    goods_name = CharField(max_length=20, default="", verbose_name="商品名称")
    goods_image = CharField(max_length=200, default="", verbose_name="商品图片")
    goods_price = DecimalField(verbose_name="商品价格")
    nums = IntegerField(default=0, verbose_name="商品数量")


if __name__ == "__main__":
    config.DB.create_tables([ShoppingCart, OrderInfo, OrderGoods])

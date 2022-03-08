from datetime import datetime

from peewee import *

from userop_srv.config import config


# 删除 - 物理删除和逻辑删除 - 物理删除  -假设你把某个用户数据 - 用户购买记录，用户的收藏记录，用户浏览记录啊
# 通过save方法做了修改如何确保只修改update_time值而不是修改add_time
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


class LeavingMessages(BaseModel):
    """
        用户留言
        """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = IntegerField(verbose_name="用户id")
    message_type = IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
                                help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = CharField(max_length=100, default="", verbose_name="主题")
    message = TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = CharField(max_length=100, verbose_name="上传的文件", help_text="上传的文件")

    class Meta:
        database = config.DB


class Address(BaseModel):
    """
    用户收货地址
    """
    user = IntegerField(verbose_name="用户id")
    province = CharField(max_length=100, default="", verbose_name="省份")
    city = CharField(max_length=100, default="", verbose_name="城市")
    district = CharField(max_length=100, default="", verbose_name="区域")
    address = CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = CharField(max_length=100, default="", verbose_name="签收人")
    signer_mobile = CharField(max_length=11, default="", verbose_name="电话")

    class Meta:
        database = config.DB


class UserFav(BaseModel):
    """
    用户收藏
    """
    user = IntegerField(verbose_name="用户id")
    goods = IntegerField(verbose_name="商品id")

    class Meta:
        database = config.DB
        primary_key = CompositeKey('user', 'goods', 'is_deleted')


if __name__ == "__main__":
    config.DB.create_tables([LeavingMessages, Address, UserFav])

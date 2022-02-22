from peewee import *
from user_srv.config import config


class BaseModel(Model):
    create_time = BigIntegerField(default=0, null=False, verbose_name="创建时间")
    update_time = BigIntegerField(default=0, null=False, verbose_name="更新时间")
    del_time = IntegerField(default=0, null=False, verbose_name="删除时间")

    class Meta:
        database = config.DB


STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用")
)


# 用户模型
class User(BaseModel):
    GENDER_CHOICES = (
        (0, "不限"),
        (1, "男"),
        (2, "女")
    )
    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=100, verbose_name="密码")
    safe_password = CharField(max_length=100, verbose_name="安全密码")
    nickname = CharField(max_length=20, default="", verbose_name="昵称")
    head_url = CharField(max_length=255, default="", verbose_name="用户头像")
    status = IntegerField(default=1, choices=STATUS_CHOICES, verbose_name="用户状态(0禁用,1启用)")
    birthday = DateField(null=True, verbose_name="出生日期")
    gender = IntegerField(choices=GENDER_CHOICES, default=0, verbose_name="性别(0不限,1男,2女)")
    orange_key = CharField(max_length=20, unique=True, null=False, verbose_name="我的推荐码")


# 后台管理员模型
class SysUser(BaseModel):
    username = CharField(max_length=20, index=True, unique=True, verbose_name="用户名")
    password = CharField(max_length=100, verbose_name="密码")
    status = IntegerField(default=1, choices=STATUS_CHOICES, verbose_name="用户状态(0禁用,1启用)")


if __name__ == '__main__':
    models = [User, SysUser]
    config.DB.create_tables(models)
    print("创建成功")

    users = User.select().limit(2).offset(1)
    for user in users:
        print(type(user.birthday))
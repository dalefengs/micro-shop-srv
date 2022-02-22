import time

import grpc
import peewee

from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.model.models import User
from user_srv.utils.utils import pbkdf2_verify, pbkdf2_encry, create_sn
from user_srv.utils.grpc_utils import response_fail
from loguru import logger


# 生成返回UserInfoRsp对象
def convert_user_to_rsp(user_rsp):
    rsp = user_pb2.UserInfoResponse()
    rsp.id = user_rsp.id
    rsp.mobile = user_rsp.mobile
    rsp.nickname = user_rsp.nickname
    rsp.gender = user_rsp.gender
    rsp.headUrl = user_rsp.head_url
    rsp.orangeKey = user_rsp.orange_key
    if user_rsp.birthday:
        rsp.birthday = int(time.mktime(user_rsp.birthday.timetuple()))
    return rsp


class UserService(user_pb2_grpc.UserServicer):
    # 获取用户列表
    def GetUserList(self, request: user_pb2.PageInfo, context):
        rsp = user_pb2.UserListResponse()
        rsp.total = User.select().count()

        offset = 0  # 偏移量
        page = 1  # 第几页
        limit = 10  # 每页显示多少条
        if request.page:
            page = request.page
        if request.limit:
            limit = request.limit
            offset = limit * (page - 1)

        users = User.select().limit(limit).offset(offset)

        for user in users:
            rsp_user_info = user_pb2.UserInfoResponse()
            rsp_user_info.id = user.id
            rsp_user_info.mobile = user.mobile
            rsp_user_info.password = user.password
            rsp_user_info.gender = user.gender
            rsp_user_info.nickname = user.nickname
            rsp_user_info.headUrl = user.head_url
            rsp_user_info.orangeKey = user.orange_key
            if user.birthday:
                rsp_user_info.birthday = int(time.mktime(user.birthday.timetuple()))
            # 不能直接赋值，需要使用 append
            rsp.data.append(rsp_user_info)
        return rsp

    # 通过手机号获取用户信息
    @logger.catch
    def GetUserInfoByMobile(self, request, context):
        try:
            user = User.get(User.mobile == request.mobile)
            return convert_user_to_rsp(user)
        except peewee.DoesNotExist:
            response_fail(context, grpc.StatusCode.NOT_FOUND, "用户不存在！")
            return user_pb2.UserInfoResponse()

    # 通过ID获取用户信息
    @logger.catch
    def GetUserInfoById(self, request, context):
        try:
            u_info = User.get_by_id(request.id)
            return convert_user_to_rsp(u_info)
        except peewee.DoesNotExist:
            response_fail(context, grpc.StatusCode.NOT_FOUND, "用户不存在")
            return user_pb2.UserInfoResponse()

    # 验证密码
    @logger.catch
    def CheckPassword(self, request, context):
        try:
            user = User.get(User.mobile == request.mobile)
        except peewee.DoesNotExist:
            response_fail(context, grpc.StatusCode.NOT_FOUND, "用户不存在")
            return user_pb2.CheckResponse(success=False)
        ok = pbkdf2_verify(user.password, request.password, user.orange_key)
        if not ok:
            response_fail(context, grpc.StatusCode.INVALID_ARGUMENT, "密码不正确!")
            return user_pb2.CheckResponse(success=False)
        return user_pb2.CheckResponse(success=True)

    # 注册用户
    def CreateUser(self, request, context):
        rs_info = user_pb2.UserInfoResponse()
        try:
            User.get(User.mobile == request.mobile)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("该手机号已经注册！")
            return rs_info
        except peewee.DoesNotExist:
            pass

        user = User()
        user.mobile = request.mobile
        user.orange_key = create_sn("L", 6)
        user.password = pbkdf2_encry(request.password, user.orange_key)
        user.create_time = time.time() * 1000

        result = user.save()
        if not result:
            response_fail(context, grpc.StatusCode.INVALID_ARGUMENT, "注册失败！")

        rs_info.mobile = user.mobile
        rs_info.orangeKey = user.orange_key
        rs_info.password = user.password
        return rs_info

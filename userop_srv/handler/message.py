from loguru import logger

from userop_srv.proto import message_pb2, message_pb2_grpc
from userop_srv.model.models import LeavingMessages


class MessageServicer(message_pb2_grpc.MessageServicer):
    @logger.catch
    def MessageList(self, request: message_pb2.MessageRequest, context):
        # 获取分类列表
        rsp = message_pb2.MessageListResponse()
        messages = LeavingMessages.select()
        if request.userId:
            messages = messages.where(LeavingMessages.user==request.userId)

        rsp.total = messages.count()
        for message in messages:
            brand_rsp = message_pb2.MessageResponse()

            brand_rsp.id = message.id
            brand_rsp.userId = message.user
            brand_rsp.messageType = message.message_type
            brand_rsp.subject = message.subject
            brand_rsp.message = message.message
            brand_rsp.file = message.file

            rsp.data.append(brand_rsp)

        return rsp

    @logger.catch
    def CreateMessage(self, request: message_pb2.MessageRequest, context):
        message = LeavingMessages()

        message.user = request.userId
        message.message_type = request.messageType
        message.subject = request.subject
        message.message = request.message
        message.file = request.file

        message.save()

        rsp = message_pb2.MessageResponse()
        rsp.id = message.id
        rsp.messageType = message.message_type
        rsp.subject = message.subject
        rsp.message = message.message
        rsp.file = message.file

        return rsp


import grpc
from loguru import logger
from peewee import DoesNotExist
from google.protobuf import empty_pb2

from userop_srv.proto import address_pb2, address_pb2_grpc
from userop_srv.model.models import Address


class AddressServicer(address_pb2_grpc.AddressServicer):
    @logger.catch
    def GetAddressList(self, request: address_pb2.AddressRequest, context):
        # 获取收货地址列表
        rsp = address_pb2.AddressListResponse()
        address = Address.select()

        if request.userId:
            address = address.where(Address.user==request.userId)

        rsp.total = address.count()
        for add in address:
            addr_rsp = address_pb2.AddressResponse()

            addr_rsp.id = add.id
            addr_rsp.userId = add.user
            addr_rsp.province = add.province
            addr_rsp.city = add.city
            addr_rsp.district = add.district
            addr_rsp.address = add.address
            addr_rsp.signerName = add.signer_name
            addr_rsp.signerMobile = add.signer_mobile

            rsp.data.append(addr_rsp)

        return rsp

    @logger.catch
    def CreateAddress(self, request: address_pb2.AddressRequest, context):
        addr = Address()

        addr.user = request.userId
        addr.province = request.province
        addr.city = request.city
        addr.district = request.district
        addr.address = request.address
        addr.signer_name = request.signerName
        addr.signer_mobile = request.signerMobile
        addr.save()

        rsp = address_pb2.AddressResponse(id=addr.id)

        return rsp

    @logger.catch
    def DeleteAddress(self, request: address_pb2.AddressRequest, context):
        try:
            address = Address.get(Address.id==request.id)
            address.delete_instance()

            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('记录不存在')
            return empty_pb2.Empty()

    @logger.catch
    def UpdateAddress(self, request: address_pb2.AddressRequest, context):
        try:
            address = Address.get(request.id)
            if request.province:
                address.province = request.province
            if request.city:
                address.city = request.city
            if request.district:
                address.district = request.district
            if request.address:
                address.address = request.address
            if request.signerName:
                address.signer_name = request.signerName
            if request.signerMobile:
                address.signer_mobile = request.signerMobile

            address.save()

            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('记录不存在')
            return empty_pb2.Empty()

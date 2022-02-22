import grpc

from user_srv.proto import user_pb2, user_pb2_grpc


class UserTest:
    def __init__(self):
        # 连接 grpc 服务器
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(page=3, limit=4))
        print(rsp.total)
        for user in rsp.data:
            print(user.mobile)


if __name__ == "__main__":
    t = UserTest()
    t.user_list()

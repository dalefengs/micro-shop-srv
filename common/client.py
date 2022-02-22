import grpc
from common.grpc_health.v1 import health_pb2,health_pb2_grpc
if __name__ == "__main__":
    with grpc.insecure_channel("192.168.200.110:50051") as channel:
        stud = health_pb2_grpc.HealthStub(channel)
        rsp: health_pb2.HealthCheckResponse = stud.Watch(health_pb2.HealthCheckRequest())
        print(rsp)

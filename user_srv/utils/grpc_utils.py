# 响应grpc状态码和信息
def response_fail(context, grpc_status_code, details):
    context.set_code(grpc_status_code)
    context.set_details(details)

import abc


# 抽象基类
class Register(metaclass=abc.ABCMeta):
    # 注册服务
    @abc.abstractmethod
    def register(self, name, id, address, port, tags, check):
        pass

    # 注销服务
    @abc.abstractmethod
    def deregister(self, service_id):
        pass

    # 获取所有服务
    @abc.abstractmethod
    def get_all_services(self):
        pass

    # 获取服务并过滤
    @abc.abstractmethod
    def filter_services(self, name):
        pass

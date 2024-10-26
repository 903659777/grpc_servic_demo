# -*- coding = utf-8 -*-
# @Time :2024/10/24 14:09
import asyncio
import uuid
import socket
from typing import Tuple

import grpc
import consul
from protos import article_pb2, article_pb2_grpc
from services.article import ArticleServer
from services.interceptors import ArticleInterceptor

client = consul.Consul("localhost", 8500)  # consul所在的ip，默认是localhost


def get_ip_port() -> Tuple[str, int]:
    """ 获取主机ip和空闲端口 """
    # 获取ip地址
    sock_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_ip.connect(("8.8.8.8", 80))
    ip = sock_ip.getsockname()[0]
    sock_ip.close()
    # 获取空闲的端口号
    sock_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_port.bind(("", 0))
    _, port = sock_port.getsockname()
    sock_port.close()
    return ip, port


def register_consul(ip: str, port: int):
    """ 注册 """
    service_id = uuid.uuid4().hex
    client.agent.service.register(
        name="grpc_servic_demo",  # 名字
        service_id=service_id,  # 注册的服务id
        address=ip,  # ip地址
        port=port,  # 端口
        tags=["servic_demo", "grpc"],  # 标签
        check=consul.Check.tcp(host=ip, port=port, interval="10s")  # 健康检查
    )
    return service_id

def deregister_consul(service_id: str):
    client.agent.service.deregister(service_id=service_id)


async def main():
    ip, port = get_ip_port()
    # server = grpc.aio.server()
    # 创建一个gRPC异步服务器实例，添加拦截器
    server = grpc.aio.server(interceptors=[ArticleInterceptor()])
    # 注册Article服务到服务器，ArticleServer是服务的具体实现
    article_pb2_grpc.add_ArticleServiceServicer_to_server(ArticleServer(), server)
    # 添加监听的ip和端口
    server.add_insecure_port(f"0.0.0.0:{port}")
    # 在服务启动之前注册 consul管理页面：http://127.0.0.1:8500
    service_id = register_consul(ip, port)
    # 启动服务器
    await server.start()
    print(f'服务器已经启动！端口：{port}')
    # 等待服务终止信号
    try:
        await server.wait_for_termination()
    finally:
        deregister_consul(service_id)  # 注销


if __name__ == '__main__':
    asyncio.run(main())

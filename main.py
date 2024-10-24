# -*- coding = utf-8 -*-
# @Time :2024/10/24 14:09
import asyncio

import grpc
from protos import article_pb2, article_pb2_grpc
from services.article import ArticleServer
from services.interceptors import ArticleInterceptor


async def main():
    # server = grpc.aio.server()
    # 创建一个gRPC异步服务器实例，添加拦截器
    server = grpc.aio.server(interceptors=[ArticleInterceptor()])
    # 注册Article服务到服务器，ArticleServer是服务的具体实现
    article_pb2_grpc.add_ArticleServiceServicer_to_server(ArticleServer(), server)
    # 添加监听的ip和端口
    server.add_insecure_port("0.0.0.0:5000")
    # 启动服务器
    await server.start()
    print('服务器已经启动！')
    # 等待服务终止信号
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(main())

# -*- coding = utf-8 -*-
# @Time :2024/10/24 15:15
import asyncio

import grpc
from protos.article_pb2_grpc import ArticleServiceStub
from protos import article_pb2

""" 这个文件是模拟客户端进行测试 """


def test_get_article_list(stub):
    # 创建了一个请求对象，在服务端方法实现的时候就是request
    request = article_pb2.ArticleListRequest()
    # 设置属性
    request.page = 1
    request.page_size = 10
    # 通过 stub 调用服务器端的 ArticleList RPC 方法，并将构造的请求对象 request 传递给这个方法。
    # 服务器端处理请求后，会返回一个响应对象，这个对象被存储在变量 response 中。
    response = stub.ArticleList(request)
    print(response)


def test_get_article_detail(stub):
    try:
        request = article_pb2.ArticleDetailRequest()
        request.pk = 5
        response = stub.ArticleDetail(request)
        print(response)
    except grpc.RpcError as e:
        print(e.code())
        print(e.details())


def test_create_article(stub):
    try:
        request = article_pb2.CreateArticleRequest()
        request.name = "活着"
        request.content = "mm"
        request.create_time = "1992-12-11"
        response = stub.CreateArticle(request)
        print(response)
    except grpc.RpcError as e:
        print(e.code())
        print(e.details())


def test_update_article(stub):
    request = article_pb2.UpdateArticleRequest()
    request.id = 1
    request.name = "西游记"
    request.content = "齐天大圣孙悟空"
    request.create_time = "2008-10-01"
    response = stub.UpdateArticle(request)
    print(response)


def test_delete_article(stub):
    request = article_pb2.DeleteArticleRequest()
    request.id = 12
    response = stub.DeleteArticle(request)
    print(response)


async def main():
    # 创建一个不加密的通道
    with grpc.insecure_channel('localhost:5000') as channel:
        # 创建了一个 ArticleServiceStub 的实例，允许客户端调用服务端定义的 RPC 方法
        stub = ArticleServiceStub(channel=channel)
        test_get_article_list(stub)
        # test_get_article_detail(stub)
        # test_create_article(stub)
        # test_update_article(stub)
        # test_delete_article(stub)


if __name__ == '__main__':
    asyncio.run(main())

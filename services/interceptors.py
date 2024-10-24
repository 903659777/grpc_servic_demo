# -*- coding = utf-8 -*-
# @Time :2024/9/16 20:02
from typing import Callable, Any

from grpc import aio as grpc_aio
from grpc_interceptor.exceptions import GrpcException
from grpc_interceptor.server import AsyncServerInterceptor
from models import AsyncSessionFactory

class ArticleInterceptor(AsyncServerInterceptor):
    """ 拦截器类似于中间件 """
    # 处理传入请求之前的预处理和传出响应之后的后处理
    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc_aio.ServicerContext,
        method_name: str,
    ) -> Any:
        session = AsyncSessionFactory()
        try:
            # 调用 gRPC 服务方法将请求发给对应方法。
            # request_or_iterator 是客户端发送的请求
            # context 是一个 ServicerContext 对象，它提供了关于 RPC 调用的信息，比如元数据（类似于http请求头）、状态码、细节信息等
            # 这里主要目的是将session发给对应方法操作数据库
            response = await method(request_or_iterator, context, session)
            return response
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
        finally:
            await session.close()

# -*- coding = utf-8 -*-
# @Time :2024/10/24 14:49
import grpc
from sqlalchemy import select, update, delete
from google.protobuf import empty_pb2

from models.article import Article
from protos import article_pb2, article_pb2_grpc


# 继承article_pb2_grpc.ArticleServiceServicer在里面实现定义好的对应方法处理服务
class ArticleServer(article_pb2_grpc.ArticleServiceServicer):
    async def ArticleList(self, request: article_pb2.ArticleListRequest, context, session):
        page = request.page
        size = request.page_size
        offset = (page - 1) * size
        async with session.begin():
            result = await session.execute(select(Article).limit(size).offset(offset))
            rows = result.scalars().all()
            # row.to_dict()是在定义映射模型的时候继承SerializerMixin，在.to_dict()可以序列化
            articles = [row.to_dict() for row in rows]
        response = article_pb2.ArticleListResponse(articles=articles)
        print("收到！")
        return response

    async def ArticleDetail(self, request: article_pb2.ArticleDetailRequest, context, session):
        article_id = request.pk
        async with session.begin():
            result = await session.execute(select(Article).where(Article.id == article_id))
            row = result.scalar()
        if not row:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('该文章不存在！')
        else:
            response = article_pb2.ArticleDetailResponse(article=row.to_dict())
            return response

    async def CreateArticle(self, request: article_pb2.CreateArticleRequest, context, session):
        name = request.name
        content = request.content
        create_time = request.create_time
        async with session.begin():
            article = Article(name=name, content=content, create_time=create_time)
            session.add(article)
        response = article_pb2.CreateArticleResponse(article=article.to_dict())
        return response

    async def UpdateArticle(self, request: article_pb2.UpdateArticleRequest, context, session):
        article_id = request.id
        name = request.name
        content = request.content
        create_time = request.create_time
        async with session.begin():
            stmt = update(Article).where(Article.id == article_id).values(name=name, content=content, create_time=create_time)
            result = await session.execute(stmt)
            rowcount = result.rowcount
        if rowcount == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"ID{article_id}不存在！")
        else:
            # 即使.proto文件定义了返回空，这里也要返回empty_pb2.Empty()
            return empty_pb2.Empty()

    async def DeleteArticle(self, request: article_pb2.DeleteArticleRequest, context, session):
        article_id = request.id
        async with session.begin():
            result = await session.execute(delete(Article).where(Article.id == article_id))
        if result.rowcount == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"ID{article_id}不存在！")
        return empty_pb2.Empty()

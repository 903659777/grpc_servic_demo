# -*- coding = utf-8 -*-
# @Time :2024/10/24 14:26
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy_serializer import SerializerMixin

from . import Base

# sqlalchemy_serializer需要安装，pip install sqlalchemy-serializer
class Article(Base, SerializerMixin):
    __tablename__ = 'article'
    # serialize_only = ('id', 'name')  # 只序列化的字段
    # serialize_rules = ('-id', "-name")  # 序列化规则，这里表示不序列化的字段
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    content = Column(Text)
    create_time = Column(DateTime)

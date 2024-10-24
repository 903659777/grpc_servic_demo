# -*- coding = utf-8 -*-
# @Time :2024/10/24 14:22
from settings import local_settings

MYSQL_HOST = local_settings.MYSQL_HOST
MYSQL_PORT = local_settings.MYSQL_PORT
MYSQL_USER = local_settings.MYSQL_USER
MYSQL_PASSWORD = local_settings.MYSQL_PASSWORD
MYSQL_DB = local_settings.MYSQL_DB

# aiomysql
# asyncmy 在保存64为的整型的时候有bug
DB_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

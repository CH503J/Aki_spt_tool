#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :about_controller.py
# @Time      :2025/7/16 08:54
# @Author    :CH503J

from common.path_utils import get_sql_path
from common.sql_utils import load_sql_queries
from service.about_service import fetch_app_info

SQL_QUERIES = load_sql_queries(get_sql_path("about_info.sql"))


def get_app_info() -> dict:
    """供 UI 层调用，获取软件信息"""
    return fetch_app_info()


if __name__ == '__main__':
    print(get_app_info())

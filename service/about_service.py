#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :about_service.py
# @Time      :2025/7/16 11:14
# @Author    :CH503J
import sqlite3

from common.path_utils import get_db_path, get_sql_path
from common.sql_utils import load_sql_queries

SQL_QUERIES = load_sql_queries(get_sql_path("about_info.sql"))


def fetch_app_info() -> dict:
    """
    从数据库 about_info 表中读取软件基本信息
    :return: 包含 app_name、version、author、github_link、example_path 的字典
    """
    db_path = get_db_path("app.db")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERIES["get_app_info"])
            row = cursor.fetchone()

            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            else:
                print("[提示] about_info 表为空")
                return {}
    except Exception as e:
        print(f"[错误] 读取 about_info 失败：{e}")
        return {}

if __name__ == '__main__':
    print(fetch_app_info())
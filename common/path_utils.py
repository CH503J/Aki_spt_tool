#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :path_utils.py
# @Time      :2025/7/8 09:58
# @Author    :CH503J
import os
import sys


def get_db_path(db_name: str = "app.db") -> str:
    """
    获取 SQLite 数据库的完整路径：
    - 开发环境：./config/DB/app.db
    - 打包环境：./config/app.db

    :param db_name:数据库名
    :return 数据库文件完整路径
    """
    base_dir = get_base_dir()
    sub_dir = "config" if is_frozen() else os.path.join("config", "DB")
    db_path = os.path.join(base_dir, sub_dir, db_name)
    return db_path


def get_sql_path(sql_file_name: str = "about_info.sql") -> str:
    """
    获取 SQL 文件路径
    - 开发环境：项目根目录下 ./sql/{sql_file_name}
    - 打包环境：安装目录下 ./sql/{sql_file_name}
    :param sql_file_name: SQL 文件名（例如 about_info.sql）
    :return: SQL 文件的完整路径
    """
    base_dir = get_base_dir()
    return os.path.join(base_dir, "sql", sql_file_name)


def is_frozen() -> bool:
    """判断是否为 PyInstaller 打包环境"""
    return getattr(sys, 'frozen', False)


def get_base_dir() -> str:
    """
    获取项目根路径：
    - 开发环境：返回源码项目根目录
    - 打包环境：返回 exe 所在目录
    """
    if is_frozen():
        return os.path.dirname(sys.executable)
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


if __name__ == '__main__':
    # 获取数据库文件路径
    print(f"当前数据库文件路径为：{get_db_path('app.db')}")
    # 获取对应sql文件路径
    print(f"当前默认SQL文件路径为：{get_sql_path()}")
    print(f"当前关于标签页SQL文件路径为：{get_sql_path('about_info.sql')}")
    print(f"当前游戏路径SQL文件路径为：{get_sql_path('game_info.sql')}")
    print(f"当前物品id SQL文件路径为：{get_sql_path('language_info.sql')}")
    print(f"当前关于标签页建表SQL文件路径为：{get_sql_path('init_about_info.sql')}")
    print(f"当前游戏路径建表SQL文件路径为：{get_sql_path('init_game_info.sql')}")
    print(f"当前物品id 建表SQL文件路径为：{get_sql_path('init_language_info.sql')}")

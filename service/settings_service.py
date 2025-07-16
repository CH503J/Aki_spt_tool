#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :settings_service.py
# @Time      :2025/7/16 11:25
# @Author    :CH503J
import sqlite3

from common.path_utils import get_db_path, get_sql_path
from common.sql_utils import load_sql_queries

SQL_QUERIES = load_sql_queries(get_sql_path("game_info.sql"))

def fetch_game_info() -> dict:
    db_path = get_db_path("app.db")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERIES["get_game_info"])
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            else:
                print("[提示] game_info 表为空")
                return {}

    except Exception as e:
        print(f"[错误] 读取 game_info 失败：{e}")
        return {}


def save_game_info(key: str, value: str) -> bool:
    """
    保存 game_info 表中的指定字段：
    - 若无记录 → 插入
    - 若已有记录 → 更新
    """
    db_path = get_db_path("app.db")
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(SQL_QUERIES["count_game_info"])
            count = cursor.fetchone()[0]

            if count == 0:
                sql = SQL_QUERIES["insert_game_info_key"].format(key=key)
                cursor.execute(sql, (value,))
                print(f"[插入成功] {key} = {value}")
            else:
                sql = SQL_QUERIES["update_game_info_key"].format(key=key)
                cursor.execute(sql, (value,))
                print(f"[更新成功] {key} = {value}")

            conn.commit()
            return True
    except Exception as e:
        print(f"[错误] 保存游戏路径失败: {e}")
        return False


if __name__ == '__main__':
    print(fetch_game_info())
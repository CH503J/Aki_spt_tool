#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :settings_service.py
# @Time      :2025/7/16 11:25
# @Author    :CH503J
import json
import os
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

def update_spt_info(path: str) -> bool:
    if not path:
        print("[错误] 未设置游戏根目录，无法获取 SPT 信息")
        return False

    spt_exe = os.path.join(path, "SPT.Server.exe")
    if not os.path.exists(spt_exe):
        print(f"[错误] 未找到文件：{spt_exe}")
        return False

    spt_server_path = os.path.abspath(spt_exe)
    spt_server_name = os.path.splitext(os.path.basename(spt_exe))[0]  # 去掉 .exe

    ok_path = save_game_info("spt_server_path", spt_server_path)
    ok_name = save_game_info("spt_server_name", spt_server_name)

    # === 获取版本号 ===
    core_json_path = os.path.join(path, "SPT_Data", "Server", "configs", "core.json")
    if not os.path.exists(core_json_path):
        print(f"[警告] 未找到 core.json，跳过版本号获取：{core_json_path}")
        ok_version = False
    else:
        try:
            with open(core_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                version = data.get("sptVersion", "").strip()
                if version:
                    ok_version = save_game_info("spt_server_version", version)
                else:
                    print("[警告] core.json 中未找到 version 字段")
                    ok_version = False
        except Exception as e:
            print(f"[错误] 解析 core.json 失败: {e}")
            ok_version = False

    return ok_path and ok_name and ok_version


if __name__ == '__main__':
    print(fetch_game_info())
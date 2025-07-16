#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :sql_utils.py
# @Time      :2025/7/15 17:59
# @Author    :CH503J

def load_sql_queries(file_path: str) -> dict:
    """
    加载 SQL 文件中的命名查询语句（支持 -- name: 标记块）
    """
    queries = {}
    current_key = None
    buffer = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()

                if stripped.startswith('-- name:'):
                    if current_key and buffer:
                        queries[current_key] = ''.join(buffer).strip()
                        buffer.clear()
                    current_key = stripped.split('-- name:', 1)[1].strip()

                elif stripped.startswith('--'):
                    # 跳过注释（非 name 标签）
                    continue

                else:
                    buffer.append(line)

            if current_key and buffer:
                queries[current_key] = ''.join(buffer).strip()

    except Exception as e:
        print(f"[错误] 读取 SQL 文件失败：{e}")

    return queries


if __name__ == '__main__':
    from common.path_utils import get_sql_path

    path = get_sql_path("about_info.sql")
    result = load_sql_queries(path)
    for k, v in result.items():
        print(f"\n[{k}]:\n{v}")

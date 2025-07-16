#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :settings_controller.py
# @Time      :2025/7/16 08:53
# @Author    :CH503J

from service.settings_service import fetch_game_info, save_game_info, update_spt_info, get_gift_code


def get_game_info() -> dict:
    """获取游戏信息"""
    return fetch_game_info()


def save_root_path(path: str) -> bool:
    """
    保存游戏根目录路径
    - 如果 game_info 表已有记录则不插入
    - 仅插入 root_path 字段（其他字段保持空或默认）

    :param path: 游戏根目录路径
    :return: 是否插入成功
    """
    if not save_spt_info(path):
        return False
    return save_game_info("root_path", path)


def save_spt_info(path: str) -> bool:
    """
    自动探测并保存 SPT 服务信息（路径 + 名称）
    - 从 game_root_path 获取 SPT.Server.exe
    - 保存 server_path 和 server_name 两个字段
    """
    if not update_spt_info(path):
        return False
    return update_spt_info(path)


def get_all_gift_code() -> set[str]:
    """获取所有礼包码"""
    return get_gift_code()
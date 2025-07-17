#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_service.py
# @Time      :2025/7/16 16:18
# @Author    :CH503J
# 全局进程句柄（用于服务控制）
import os
import subprocess

from common.message_utils import message_notice
from controller.settings_controller import get_game_info

spt_process = None
fika_process = None


def start_spt_server():
    global spt_process
    spt_path = get_game_info().get("spt_server_path")
    if not spt_path or not os.path.exists(spt_path):
        message_notice(message="请先配置SPT游戏路径", level="error")
        return None

    try:
        process = subprocess.Popen(
            [spt_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            bufsize=1,
            cwd=os.path.dirname(spt_path)
        )
        spt_process = process
        message_notice(message="SPT服务已启动")
        return  process
    except Exception as e:
        message_notice(message=f"SPT服务启动失败{e}", level="error")
        return None



def stop_spt_server():
    print("spt server 停止功能暂未实现")


def start_fika_server():
    print("fika server 启动功能暂未实现")


def stop_fika_server():
    print("fika server 停止功能暂未实现")


if __name__ == '__main__':
    start_spt_server()

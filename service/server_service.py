#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_service.py
# @Time      :2025/7/16 16:18
# @Author    :CH503J
# 全局进程句柄（用于服务控制）
import os
import subprocess

from common.message_utils import to_message
from controller.settings_controller import get_game_info

spt_process = None
fika_process = None


def start_spt_server():
    global spt_process
    spt_path = get_game_info().get("spt_server_path")
    if not spt_path or not os.path.exists(spt_path):
        to_message(message="请先配置SPT游戏路径", level="error")
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
        to_message(message="SPT服务已启动")
        return process
    except Exception as e:
        to_message(message=f"SPT服务启动失败{e}", level="error")
        return None


def stop_spt_server():
    global spt_process
    if spt_process and spt_process.poll() is None:
        try:
            spt_process.terminate()
            spt_process.wait(timeout=5)
            to_message(message="SPT服务已停止")
        except Exception as e:
            to_message(message=f"SPT服务停止失败{e}", level="error")
            to_message(message=f"正在强制停止SPT服务", level="warning")
            try:
                spt_process.kill()
                to_message(message="SPT服务已强制停止", level="info")
            except Exception as e:
                to_message(message=f"SPT服务强制停止失败{e}", level="error")
    else:
        to_message(message="SPT服务未运行", level="warning")


def start_fika_server():
    print("fika server 启动功能暂未实现")


def stop_fika_server():
    print("fika server 停止功能暂未实现")

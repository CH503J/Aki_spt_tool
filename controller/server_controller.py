#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_controller.py
# @Time      :2025/7/16 16:18
# @Author    :CH503J
from service.server_service import (
    start_spt_server,
    stop_spt_server,
    start_fika_server,
    stop_fika_server
)


def start_spt():
    start_spt_server()


def stop_spt():
    stop_spt_server()


def start_fika():
    start_fika_server()


def stop_fika():
    stop_fika_server()

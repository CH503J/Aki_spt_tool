#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :global_store.py
# @Time      :2025/7/17 15:09
# @Author    :CH503J
_main_window = None


def set_main_window(window):
    global _main_window
    _main_window = window


def get_main_window():
    return _main_window

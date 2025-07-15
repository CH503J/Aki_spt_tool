#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :home_ui.py
# @Time      :2025/7/15 13:58
# @Author    :CH503J
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton)

from common.toast_utils import show_toast
from ui.about_ui import AboutTab
from ui.search_ui import SearchTab
from ui.server_ui import ServerTab


class HomeWindow(QMainWindow):
    """
    应用程序主窗口
    - 包含多标签页界面（启停页、搜索页、关于页）
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Launcher 主界面")
        self.setGeometry(100, 100, 1200, 600)

        # 创建主标签页控件
        tabs = QTabWidget()
        tabs.addTab(ServerTab(), "启停")

        tabs.addTab(SearchTab(), "搜索")

        tabs.addTab(AboutTab(), "关于")

        tabs.addTab(ToastTest(), "测试")

        # 设置中央布局
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


class ToastTest(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("这是测试页"))

        # 添加按钮用于触发通知
        btn = QPushButton("点击我推送通知")
        btn.clicked.connect(lambda: show_toast(self.window(), "程序正在做事..."))
        layout.addWidget(btn)

        self.setLayout(layout)

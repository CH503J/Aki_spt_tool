#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :home_ui.py
# @Time      :2025/7/15 13:58
# @Author    :CH503J
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton)

from common.message_utils import to_message
from ui.about_ui import AboutTab
from ui.quest_ui import QuestTab
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
        self.setGeometry(100, 100, 1000, 500)
        self.center()

        # 创建主标签页控件
        tabs = QTabWidget()
        tabs.addTab(ServerTab(), "启停")

        tabs.addTab(SearchTab(), "搜索")

        tabs.addTab(QuestTab(), "任务")

        tabs.addTab(ToastTest(), "测试")

        tabs.addTab(AboutTab(), "关于")

        # 设置中央布局
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def center(self):
        """将窗口移动到屏幕中心"""
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)


# 测试标签页，调试气泡消息通知用
class ToastTest(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("这是测试页"))

        # 添加按钮用于触发通知
        btn = QPushButton("点击我推送通知")
        btn.clicked.connect(lambda: to_message("这是测试页气泡", 5000, level="error"))
        layout.addWidget(btn)

        self.setLayout(layout)

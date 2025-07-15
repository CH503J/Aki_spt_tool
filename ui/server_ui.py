#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_ui.py
# @Time      :2025/7/15 13:58
# @Author    :CH503J
from PyQt6.QtWidgets import (QVBoxLayout, QLabel, QWidget, QPushButton)

from common.message_utils import message_notice


class ServerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这是启停页"))

        btn = QPushButton("启动服务")
        btn.clicked.connect(lambda: message_notice(self.window(), "启动服务成功！", 5000, level="success"))
        layout.addWidget(btn)

        self.setLayout(layout)

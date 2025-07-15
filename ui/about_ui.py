#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :about_ui.py
# @Time      :2025/7/15 14:00
# @Author    :CH503J
from PyQt6.QtWidgets import (QVBoxLayout, QLabel, QWidget, QPushButton)

from common.message_utils import message_notice


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这是关于页"))

        btn = QPushButton("关于页气泡测试")
        btn.clicked.connect(lambda: message_notice(self.window(), "这是关于页气泡测试"))
        layout.addWidget(btn)
        self.setLayout(layout)

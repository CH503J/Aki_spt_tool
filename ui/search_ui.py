#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :search_ui.py
# @Time      :2025/7/15 13:59
# @Author    :CH503J
from PyQt6.QtWidgets import (QVBoxLayout, QLabel, QWidget, QPushButton)

from common.message_utils import message_notice


class SearchTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这是搜索页"))

        btn = QPushButton("搜索页气泡")
        btn.clicked.connect(lambda :message_notice("这是搜索页气泡", 5000, level="warning"))
        layout.addWidget(btn)
        self.setLayout(layout)

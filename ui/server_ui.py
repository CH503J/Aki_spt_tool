#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_ui.py
# @Time      :2025/7/15 13:58
# @Author    :CH503J


from PyQt6.QtWidgets import ( QVBoxLayout, QLabel, QWidget )


class ServerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这是启停页"))
        self.setLayout(layout)
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :search_ui.py
# @Time      :2025/7/15 13:59
# @Author    :CH503J


from PyQt6.QtWidgets import ( QVBoxLayout, QLabel, QWidget )


class SearchTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这是搜索页"))
        self.setLayout(layout)
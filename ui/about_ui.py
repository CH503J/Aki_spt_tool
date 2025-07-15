#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :about_ui.py
# @Time      :2025/7/15 14:00
# @Author    :CH503J


from PyQt6.QtWidgets import ( QVBoxLayout, QLabel, QWidget )


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这是关于页"))
        self.setLayout(layout)

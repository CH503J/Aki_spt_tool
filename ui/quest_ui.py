#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :quest_ui.py
# @Time      :2025/7/17 09:50
# @Author    :CH503J
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QFrame, QGridLayout

from common.message_utils import message_notice


class QuestTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # === 商人列表 ===
        self.traders = [
            {"name": "Prapor：毛商", "img": "icon/59b91ca086f77469a81232e4.png"},
            {"name": "Therapist：医生大妈", "img": "icon/59b91cab86f77469aa5343ca.png"},
            {"name": "Skier：滑雪者", "img": "icon/59b91cb486f77469a81232e5.png"},
            {"name": "Peacekeeper：美商", "img": "icon/59b91cbd86f77469aa5343cb.png"},
            {"name": "Mechanic：机械师", "img": "icon/5a7c2ebb86f7746e324a06ab.png"},
            {"name": "Ragman：服装师", "img": "icon/5ac3b86a86f77461491d1ad8.png"},
            {"name": "Jaeger：老贱人", "img": "icon/5c06531a86f7746319710e1b.png"},
            {"name": "Fence：黑商", "img": "icon/579dc571d53a0658a154fbec.png"},
            {"name": "Lightkeeper：灯塔商人", "img": "icon/638f541a29ffd1183d187f57.png"},
            {"name": "装甲车车长", "img": "icon/656f0f98d80a697f855d34b1.png"},
            {"name": "竞技场商人", "img": "icon/6617beeaa9cfa777ca915b7c.png"},
        ]

        # === 顶部商人头像区域 ===
        trader_frame = QFrame()
        trader_frame.setFixedHeight(80)
        trader_layout = QGridLayout(trader_frame)
        trader_layout.setContentsMargins(0, 0, 0, 0)
        trader_layout.setSpacing(15)
        trader_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        for i, trader in enumerate(self.traders):
            avatar_container = QVBoxLayout()
            avatar_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

            avatar_button = QPushButton()
            avatar_button.setFixedSize(75, 75)
            avatar_button.setToolTip(trader["name"])
            avatar_button.setStyleSheet("""
                QPushButton {
                    border: 2px dashed #999;
                    background-color: #f0f0f0;
                }
                QPushButton:hover {
                    border-color: #007acc;
                }
            """)

            pixmap = QPixmap(trader["img"])
            scaled = pixmap.scaled(
                avatar_button.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            avatar_button.setIcon(QIcon(scaled))
            avatar_button.setIconSize(avatar_button.size())

            # 绑定点击事件
            avatar_button.clicked.connect(partial(self.show_trader_quests, trader))

            avatar_container.addWidget(avatar_button)

            container_widget = QWidget()
            container_widget.setLayout(avatar_container)

            row = i // 11
            col = i % 11
            trader_layout.addWidget(container_widget, row, col)

        layout.addWidget(trader_frame)

        # === 下方任务详情区域 ===
        quest_detail_frame = QFrame()
        quest_detail_layout = QVBoxLayout(quest_detail_frame)

        self.quest_detail_label = QLabel("任务详情占位：请从数据库加载任务信息")
        self.quest_detail_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.quest_detail_label.setWordWrap(True)
        quest_detail_layout.addWidget(self.quest_detail_label)

        layout.addWidget(quest_detail_frame)

        # === 调试按钮 ===
        btn = QPushButton("任务页气泡")
        btn.clicked.connect(lambda: message_notice(self.window(), "这是任务页气泡", 3000, "info"))
        layout.addWidget(btn)

        self.setLayout(layout)

    def show_trader_quests(self, trader: dict):
        # 点击头像时更新下方任务区域内容
        self.quest_detail_label.setText(f"{trader['name']} 的任务信息展示（占位）")
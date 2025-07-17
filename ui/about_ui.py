#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :about_ui.py
# @Time      :2025/7/15 14:00
# @Author    :CH503J


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout,
    QLineEdit, QPushButton, QHBoxLayout, QFileDialog, QGridLayout
)

from common.message_utils import to_message
from controller.about_controller import get_app_info
from controller.settings_controller import save_root_path, get_game_info, get_all_gift_code


def copy_to_clipboard(text: str):
    """点击即复制"""
    from PyQt6.QtGui import QGuiApplication
    QGuiApplication.clipboard().setText(text)
    print(f"[复制成功] {text}")
    to_message(f"礼包码 {text} 已复制到剪贴板！")


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.gift_list = None
        self.label_name = None
        self.label_version = None
        self.label_author = None
        self.github_label = None
        self.input_path = None
        self.gift_layout = None
        self.init_ui()
        self.load_root_path()

    def init_ui(self):
        app_info = get_app_info()
        layout = QVBoxLayout()

        # --- 关于软件区域 ---
        about_group = QGroupBox("关于软件")
        about_layout = QVBoxLayout()

        self.label_name = QLabel(f"软件名称：{app_info.get('app_name', '未知')}")
        self.label_version = QLabel(f"版本号：{app_info.get('version', '未知')}")
        self.label_author = QLabel(f"开发者：{app_info.get('author', '未知')}")

        self.github_label = QLabel(f"<a href='{app_info.get('github_link', 'https://github.com/')}'>🌐 GitHub 主页</a>")
        self.github_label.setOpenExternalLinks(True)
        self.github_label.setStyleSheet("QLabel { color: #1e90ff; font-size: 14px; }")

        about_layout.addWidget(self.label_name)
        about_layout.addWidget(self.label_version)
        about_layout.addWidget(self.label_author)
        about_layout.addWidget(self.github_label)

        about_group.setLayout(about_layout)

        # --- 设置区域 ---
        settings_group = QGroupBox("软件设置")
        form_layout = QFormLayout()

        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("请输入路径...")

        btn_select = QPushButton("选择路径")
        btn_select.clicked.connect(self.select_path)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.input_path)
        path_layout.addWidget(btn_select)

        btn_save = QPushButton("保存设置")
        btn_save.clicked.connect(self.save_path)

        form_layout.addRow("游戏根目录：", path_layout)
        form_layout.addRow(btn_save)

        settings_group.setLayout(form_layout)

        # --- 礼包码区域 ---
        self.gift_list = get_all_gift_code()
        if len(self.gift_list) == 0:
            to_message("未找到任何礼包码！", 5000, "warning")
        gift_group = QGroupBox(f"礼包码（{len(self.gift_list)}）")
        gift_group.setToolTip("点击礼包码即可复制")
        self.gift_layout = QGridLayout()
        gift_group.setLayout(self.gift_layout)

        # TODO: 后续动态添加按钮

        for i, gift_code in enumerate(self.gift_list):
            btn = QPushButton(gift_code)
            btn.clicked.connect(lambda _, v=gift_code: copy_to_clipboard(v))
            row, col = divmod(i, 5)
            self.gift_layout.addWidget(btn, row, col)

        # --- 主布局整合 ---
        layout.addWidget(about_group)
        layout.addWidget(settings_group)
        layout.addWidget(gift_group)
        layout.addStretch()
        self.setLayout(layout)

    # 选择游戏根目录
    def select_path(self):
        current = self.input_path.text().strip()
        folder = QFileDialog.getExistingDirectory(self, "选择游戏根目录", current or "")
        if folder:
            self.input_path.setText(folder)

    # 保存游戏根目录
    def save_path(self):
        path = self.input_path.text().strip()
        if not path:
            to_message("请选择正确的游戏根目录！", 5000, "error")
            return

        success = save_root_path(path)
        if success:
            to_message("保存成功！")
        else:
            to_message("请选择正确的游戏根目录！", 5000, "error")

    # 获取游戏根目录
    def load_root_path(self):
        root_path = get_game_info().get("root_path")
        if not root_path:
            to_message("请选择正确的游戏根目录！", 5000, "warning")
        self.input_path.setText(root_path)

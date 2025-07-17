#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :server_ui.py
# @Time      :2025/7/15 13:58
# @Author    :CH503J
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QCheckBox
)

from common.message_utils import message_notice
from controller.server_controller import (
    start_spt,
    start_fika,
    stop_spt,
    stop_fika
)


class StatusIndicator(QLabel):
    """圆形状态指示灯控件"""

    def __init__(self, color="red", diameter=20, parent=None):
        super().__init__(parent)
        self._color = color
        self._diameter = diameter
        self.setFixedSize(diameter, diameter)

    def set_color(self, color: str):
        """设置指示灯颜色，并自动更新 tooltip"""
        self._color = color
        self.update()  # 重绘

        # 状态提示映射
        status_tooltips = {
            "red": "服务状态：未运行",
            "green": "服务状态：正常运行",
            "orange": "服务状态：运行出错",
            "gray": "服务状态：未知"
        }

        self.setToolTip(status_tooltips.get(color, "服务状态：未知"))

    def paintEvent(self, event):
        """绘制圆形指示灯"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self._color))
        painter.setPen(Qt.PenStyle.NoPen)

        # 为了视觉更舒服，稍微缩进一点绘制（可选）
        margin = 2
        painter.drawEllipse(
            margin,
            margin,
            self._diameter - 2 * margin,
            self._diameter - 2 * margin
        )


class ServerTab(QWidget):
    """
    启动器页面 UI 类
    包含服务启动控制按钮、日志输出框、状态标签
    """

    def __init__(self, parent=None):
        """
        :param parent: 主窗口 MainWindow，用于传入控制器做弹窗提示
        """
        super().__init__(parent)
        self.status_indicator = None
        self.status_label = None
        self.fika_server_log_output = None
        self.server_log_output = None
        self.headless_log_output = None
        self.log_all_checkbox = None
        self.start_button = None
        self.stop_button = None
        self.main_window = parent
        self.controller = None
        self.init_ui()
        self.init_controller()

    def init_ui(self):
        """初始化 UI 控件与布局"""
        layout = QVBoxLayout()

        # 上层日志： Fika.Server 日志框，占据整行
        self.fika_server_log_output = QTextEdit()
        self.fika_server_log_output.setReadOnly(True)
        self.fika_server_log_output.setFixedHeight(80)
        self.fika_server_log_output.setPlaceholderText("Fika.Server 日志...")

        # 下层日志：SPT 日志 + Headless（预留）
        self.server_log_output = QTextEdit()
        self.server_log_output.setReadOnly(True)
        self.server_log_output.setPlaceholderText("SPT.Server 日志...")

        self.headless_log_output = QTextEdit()
        self.headless_log_output.setReadOnly(True)
        self.headless_log_output.setPlaceholderText("Fika.Headless 日志...")

        top_log_row = QHBoxLayout()
        top_log_row.addWidget(self.fika_server_log_output)

        bottom_log_row = QHBoxLayout()
        bottom_log_row.addWidget(self.server_log_output)
        bottom_log_row.addWidget(self.headless_log_output)

        # 状态灯 + 控制按钮
        self.status_indicator = StatusIndicator()
        self.status_indicator.set_color("red")

        self.start_fika_checkbox = QCheckBox("启动Fika")
        self.start_fika_checkbox.setChecked(False)
        self.start_fika_checkbox.setToolTip("勾选后启动服务时一并启动 Fika.Server")

        # 控制按钮区
        self.log_all_checkbox = QCheckBox("全部日志")
        self.log_all_checkbox.setChecked(True)
        self.log_all_checkbox.setToolTip("勾选后将输出所有日志，包括 info/debug")

        self.start_button = QPushButton("启动服务")
        self.stop_button = QPushButton("停止服务")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.status_indicator)
        button_layout.addWidget(self.start_fika_checkbox)
        button_layout.addWidget(self.log_all_checkbox)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()

        # 页面整体布局组装
        layout.addLayout(top_log_row)
        layout.addLayout(bottom_log_row)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 信号连接
        self.start_button.clicked.connect(self.start)
        # self.stop_button.clicked.connect(self.stop)
        # self.start_button.clicked.connect(
        #     lambda: message_notice("启动服务功能暂未实现", duration=3000, level="error"))
        self.stop_button.clicked.connect(
            lambda: message_notice("关闭服务功能暂未实现", duration=3000, level="error"))

    def init_controller(self):
        """初始化启动器控制器"""
        pass

    def start(self):
        """启动服务（由控制器控制）"""
        start_spt()
        start_fika()

    def stop(self):
        """停止服务（由控制器控制）"""
        stop_spt()
        stop_fika()

    def append_log(self, text, source="server"):
        """
        追加日志到对应日志窗口
        :param text: 日志内容
        :param source: 日志来源，支持 "program" / "fika" / "server"
        """
        if source == "fika":
            self.fika_server_log_output.append(text)
            self.fika_server_log_output.verticalScrollBar().setValue(
                self.fika_server_log_output.verticalScrollBar().maximum()
            )
        else:
            self.server_log_output.append(text)
            self.server_log_output.verticalScrollBar().setValue(
                self.server_log_output.verticalScrollBar().maximum()
            )

    def update_status_light(self, status: str):
        """
        更新服务状态灯颜色
        :param status: "stopped" | "running" | "error"
        """
        color = {
            "stopped": "red",
            "running": "green",
            "error": "orange"
        }.get(status, "gray")

        self.status_indicator.set_color(color)

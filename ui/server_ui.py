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
        self._color = color
        self.update()

        status_tooltips = {
            "red": "服务状态：未运行",
            "green": "服务状态：正常运行",
            "orange": "服务状态：运行出错",
            "gray": "服务状态：未知"
        }
        self.setToolTip(status_tooltips.get(color, "服务状态：未知"))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self._color))
        painter.setPen(Qt.PenStyle.NoPen)
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
        super().__init__(parent)
        self.start_fika_checkbox = None
        self.status_indicator = None
        self.fika_server_log_output = None
        self.server_log_output = None
        self.headless_log_output = None
        self.log_all_checkbox = None
        self.start_button = None
        self.stop_button = None
        self.main_window = parent
        self.controller = None

        # 新增 layout 成员变量
        self.top_log_row = QHBoxLayout()
        self.bottom_log_row = QHBoxLayout()

        self.init_ui()
        self.init_controller()

    def init_ui(self):
        layout = QVBoxLayout()

        self.fika_server_log_output = QTextEdit()
        self.fika_server_log_output.setReadOnly(True)
        self.fika_server_log_output.setFixedHeight(60)
        self.fika_server_log_output.setPlaceholderText("Fika.Server 日志...")

        self.server_log_output = QTextEdit()
        self.server_log_output.setReadOnly(True)
        self.server_log_output.setPlaceholderText("SPT.Server 日志...")

        self.headless_log_output = QTextEdit()
        self.headless_log_output.setReadOnly(True)
        self.headless_log_output.setPlaceholderText("Fika.Headless 日志...")

        # 初始添加控件（注意此处不做逻辑判断）
        self.top_log_row.addWidget(self.server_log_output)
        self.top_log_row.addWidget(self.headless_log_output)
        self.bottom_log_row.addWidget(self.fika_server_log_output)

        # 状态灯 + 控制区
        self.status_indicator = StatusIndicator()
        self.status_indicator.set_color("red")

        self.start_fika_checkbox = QCheckBox("启动Fika")
        self.start_fika_checkbox.setChecked(False)
        self.start_fika_checkbox.setToolTip("勾选后启动服务时一并启动 Fika.Server")
        self.start_fika_checkbox.stateChanged.connect(self.update_log_layout)

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

        # 页面整体组装
        layout.addLayout(self.top_log_row)
        layout.addLayout(self.bottom_log_row)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        self.update_log_layout()  # 初始化布局状态

    def update_log_layout(self):
        """根据“启动Fika”勾选状态动态调整日志布局"""
        fika_enabled = self.start_fika_checkbox.isChecked()

        for layout in [self.top_log_row, self.bottom_log_row]:
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i)
                widget = item.widget()
                if widget:
                    widget.setParent(None)

        if fika_enabled:
            self.top_log_row.addWidget(self.server_log_output)
            self.top_log_row.addWidget(self.headless_log_output)
            self.bottom_log_row.addWidget(self.fika_server_log_output)
        else:
            self.top_log_row.addWidget(self.server_log_output)
            # 不显示 Fika 和 Headless

    def init_controller(self):
        """初始化控制器（预留）"""
        pass

    def start(self):
        """启动服务（控制逻辑）"""
        start_spt()
        if self.start_fika_checkbox.isChecked():
            start_fika()

    def stop(self):
        stop_spt()
        if self.start_fika_checkbox.isChecked():
            stop_fika()

    def append_log(self, text, source="server"):
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
        color = {
            "stopped": "red",
            "running": "green",
            "error": "orange"
        }.get(status, "gray")

        self.status_indicator.set_color(color)

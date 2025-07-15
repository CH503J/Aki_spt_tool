#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :message_utils.py
# @Time      :2025/7/15 15:22
# @Author    :CH503J
from PyQt6.QtWidgets import QLabel, QApplication, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QObject

# 文本颜色 + emoji 映射
LEVEL_STYLE = {
    "info":    {"emoji": "ℹ️",  "color": "#00A6ED"},
    "success": {"emoji": "✅",  "color": "#00D26A"},
    "warning": {"emoji": "⚠️",  "color": "#FFB02E"},
    "error":   {"emoji": "❌",  "color": "#F92F60"},
}

class MessageManager(QObject):
    """管理所有消息气泡的叠加与位置"""
    _instances = {}

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.active_toasts = []

    @classmethod
    def get(cls, parent_widget):
        if parent_widget not in cls._instances:
            cls._instances[parent_widget] = MessageManager(parent_widget)
        return cls._instances[parent_widget]

    def show_toast(self, message: str, duration: int = 3000, level: str = "info"):
        # 获取 emoji 与文字颜色
        config = LEVEL_STYLE.get(level, LEVEL_STYLE["info"])
        emoji = config["emoji"]
        color = config["color"]

        toast = QLabel(f"{emoji}  {message}", self.parent)
        toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toast.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # 判断深色模式
        palette = QApplication.palette()
        bg_color = palette.color(palette.ColorRole.Window)
        is_dark_mode = bg_color.value() < 128

        # 背景样式跟随系统，文本颜色根据 level 设置
        if is_dark_mode:
            bg = "#444"
            border = "none"
        else:
            bg = "#eee"
            border = "1px solid #aaa"

        style = f"""
            QLabel {{
                background-color: {bg};
                color: {color};
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                border: {border};
            }}
        """
        toast.setStyleSheet(style)

        # 淡出效果
        effect = QGraphicsOpacityEffect()
        toast.setGraphicsEffect(effect)
        effect.setOpacity(1.0)

        toast.adjustSize()
        self.active_toasts.append(toast)
        self.relayout_toasts()

        toast.show()

        # 延迟淡出动画
        def start_fade():
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(1000)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)

            def on_finished():
                toast.deleteLater()
                if toast in self.active_toasts:
                    self.active_toasts.remove(toast)
                    self.relayout_toasts()

            anim.finished.connect(on_finished)
            anim.start()
            toast._anim = anim  # 避免被垃圾回收

        QTimer.singleShot(duration - 1000, start_fade)

    def relayout_toasts(self):
        """重新排列所有当前 toast 的位置"""
        margin = 20
        spacing = 10
        x = self.parent.width() - margin
        y = margin

        for toast in self.active_toasts:
            toast.adjustSize()
            toast.move(x - toast.width(), y)
            y += toast.height() + spacing


def message_notice(parent_widget, message: str, duration: int = 3000, level: str = "info"):
    """
        显示消息提示气泡

        参数:
            parent_widget (QWidget): 父级控件，用于定位消息提示的位置\n
            message (str): 要显示的消息文本\n
            duration (int): 消息显示持续时间(毫秒)，默认3000ms\n
            level (str): 消息级别，可选值: info/success/warning/error，默认info
        功能:
            根据消息级别显示带对应图标和颜色的提示框\n
            支持深色/浅色模式自动适配\n
            多个消息会垂直堆叠显示\n
            自动处理消息的淡入淡出动画效果\n
        """
    manager = MessageManager.get(parent_widget)
    manager.show_toast(message, duration, level)
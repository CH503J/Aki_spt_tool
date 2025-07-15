#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :message_utils.py
# @Time      :2025/7/15 15:22
# @Author    :CH503J
from PyQt6.QtWidgets import QLabel, QApplication, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QObject


class MessageManager(QObject):
    """管理所有消息气泡的叠加与位置"""
    _instances = {}  # 每个窗口独立一个

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.active_toasts = []  # 当前所有显示中的气泡

    @classmethod
    def get(cls, parent_widget):
        if parent_widget not in cls._instances:
            cls._instances[parent_widget] = MessageManager(parent_widget)
        return cls._instances[parent_widget]

    def show_toast(self, message: str, duration: int = 3000):
        toast = QLabel(message, self.parent)
        toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toast.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # 判断深色模式
        palette = QApplication.palette()
        bg_color = palette.color(palette.ColorRole.Window)
        is_dark_mode = bg_color.value() < 128

        # 样式适配
        if is_dark_mode:
            style = """
                QLabel {
                    background-color: #444;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-size: 14px;
                }
            """
        else:
            style = """
                QLabel {
                    background-color: #eee;
                    color: black;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-size: 14px;
                    border: 1px solid #aaa;
                }
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

        # 淡出 + 删除
        def start_fade():
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(1000)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)

            def on_finished():
                toast.deleteLater()
                self.active_toasts.remove(toast)
                self.relayout_toasts()

            anim.finished.connect(on_finished)
            anim.start()
            toast._anim = anim  # 防止被GC

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


def message_notice(parent_widget, message: str, duration: int = 3000):
    manager = MessageManager.get(parent_widget)
    manager.show_toast(message, duration)

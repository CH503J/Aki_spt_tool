#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :message_utils.py
# @Time      :2025/7/15 15:22
# @Author    :CH503J
from PyQt6.QtWidgets import QLabel, QApplication, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation


def message_notice(parent_widget, message: str, duration: int = 3000):
    """
    在 parent_widget 内部显示一个自动消失的气泡提示（带淡出动画，支持深浅色适配）
    """
    toast = QLabel(message, parent_widget)
    toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
    toast.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    # 判断深色模式（根据当前窗口调色板背景）
    palette = QApplication.palette()
    bg_color = palette.color(palette.ColorRole.Window)
    is_dark_mode = bg_color.value() < 128

    # 设置样式（深浅色自动适配）
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

    # 设置淡出动画效果
    effect = QGraphicsOpacityEffect()
    toast.setGraphicsEffect(effect)
    effect.setOpacity(1.0)

    # 放置在主 widget 右上角（非全屏，安全）
    toast.adjustSize()
    margin = 20
    x = parent_widget.width() - toast.width() - margin
    y = margin
    toast.move(x, y)
    toast.show()

    # 2 秒后开始淡出（1秒动画）
    def start_fade():
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(1000)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.finished.connect(toast.deleteLater)
        anim.start()
        toast._anim = anim  # 防止被 GC

    QTimer.singleShot(duration - 1000, start_fade)

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :toast_utils.py
# @Time      :2025/7/15 15:22
# @Author    :CH503J


from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation


# todo 1、 气泡不随窗口移动；2、 气泡展示优先级太高（始终顶层展示）
def show_toast(parent, message: str, duration: int = 3000):
    """
    显示自动消失的气泡通知，支持淡出动画 & 深浅主题适配
    会出现在主窗口右上角（屏幕坐标系），跟随窗口位置变化而变化
    """
    toast = QLabel(message)
    toast.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # 判断当前主题
    palette = QApplication.palette()
    bg_color = palette.color(palette.ColorRole.Window)
    is_dark_mode = bg_color.value() < 128

    # 样式
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
    toast.adjustSize()

    # 设置窗口属性
    toast.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.Tool |
        Qt.WindowType.WindowStaysOnTopHint
    )
    toast.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    toast.setWindowOpacity(1.0)

    # 获取主窗口在屏幕上的位置，并据此放置气泡
    margin = 20
    parent_pos = parent.mapToGlobal(parent.rect().topRight())
    x = parent_pos.x() - toast.width() - margin
    y = parent_pos.y() + margin
    toast.move(x, y)

    toast.show()

    # 淡出动画（最后1秒）
    def fade_out():
        anim = QPropertyAnimation(toast, b"windowOpacity")
        anim.setDuration(1000)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.start()
        anim.finished.connect(toast.close)
        toast._anim = anim

    QTimer.singleShot(duration - 1000, fade_out)

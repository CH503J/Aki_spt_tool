#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName   :main.py
# @Time       :2025/7/15 13:56
# @Author     :CH503J
# @ProjectName:Aki_spt_tool
import sys

from PyQt6.QtWidgets import QApplication

from ui.home_ui import HomeWindow

# 获取项目结构命令   tree /F > structure.txt
if __name__ == '__main__':
    print("================================= AKI SPT TOOL =================================")
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())
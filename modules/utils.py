# -*- coding: utf-8 -*-
"""Utilities."""


class PyQTCheck:
    try:
        __import__('PyQt5')
        pyqt5 = True
    except ImportError:
        pyqt5 = False

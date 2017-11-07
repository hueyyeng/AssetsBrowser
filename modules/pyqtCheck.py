try:
    __import__('PyQt5')
    pyqt5 = True
except ImportError:
    pyqt5 = False
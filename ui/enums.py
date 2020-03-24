"""UI Enums"""
from enum import Enum

from config.configurations import get_setting


class PreviewRadio(Enum):
    SMALL = -2
    BIG = -3
    CUSTOM = -4

    def size(self):
        # https://github.com/PyCQA/pylint/issues/2306#issuecomment-524554162
        value = int(self.value)
        if value == -2:
            return 150
        if value == -3:
            return 300
        if value == -4:
            return get_setting('Advanced', 'PreviewCustomMaxSize')


class IconRadio(Enum):
    ENABLE = -2
    DISABLE = -3
    GENERIC = -4


class ThemeRadio(Enum):
    LIGHT = -2
    DARK = -3


class SeparatorCombo(Enum):
    UNDERSCORE = 0
    DASH = 1


class PrefixRadio(Enum):
    FIRST = -2
    WHOLE = -3


class SuffixRadio(Enum):
    VERSION = -2
    CUSTOM = -3


class FontRadio(Enum):
    DEFAULT = -2
    MONOSPACE = -3
    CUSTOM = -4

    def font(self):
        value = int(self.value)
        if value == -2:
            return 'sans-serif'
        if value == -3:
            return 'monospace'


class FontSize(Enum):
    DEFAULT = 12
    TINY = 10
    LARGE = 16

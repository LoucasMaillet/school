# coding: utf-8
"""Enum declaration module
"""


# Typing
from enum import StrEnum


class Class(StrEnum):
    # For UI class name
    ACTIVE = "active"
    UNACTIVE = "unactive"
    DEFAULT = "default"
    HIDE = "hide"
    OVER = "over"


class KeyEvent(StrEnum):
    # Keyboard events
    CTRL_Z = "<Control-z>"
    CTRL_MAJ_Z = "<Control-Z>"
    UP = "<Up>"
    DOWN = "<Down>"
    LEFT = "<Left>"
    RIGHT = "<Right>"


class MouseEvent(StrEnum):
    # Mouse events
    ONCLICK = "<Button-1>"
    ONPRESS = "<ButtonPress-1>"
    ONRELEASE = "<ButtonRelease-1>"

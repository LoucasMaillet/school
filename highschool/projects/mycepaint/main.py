#!/usr/bin/python3

__author__ = "Lucas Maillet"

import pygame as pg
import datetime as dt

from tkinter import filedialog as fd

# Alias
dis = pg.display
evh = pg.event
img = pg.image

# Colors
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
MAGENTA = 255, 0, 255
CYAN = 0, 255, 255

# Windows parameters
WIN_SIZE = 700, 400
WIN_BACK = WHITE

# Line tools parameter
MAX_UNDO = MAX_REDO = 10000
MIN_LI_WIDTH = 1
DEFAULT_LINE_COLOR = BLACK
DEFAULT_LINE_WIDTH = MIN_LI_WIDTH
COLOR_FORMAT = "RGB"
KEY_MAP_COLOR = {
    'N': BLACK,
    'W': WHITE,
    'R': RED,
    'G': GREEN,
    'B': BLUE,
    'J': YELLOW,
    'M': MAGENTA,
    'C': CYAN,
}
FILE_DIALOG = {
    "defaultextension": "png",
    "filetypes": (
        ("PNG files", "*.png"),
        ("All Files", "*.*")
    )
}


class Pile(list):

    """An undo/redo pile"""

    __top: int

    def __init__(self, top: int):
        self.__top = top

    def pack(self, item: any):
        if len(self) >= self.__top:
            self.pop(0)
        self.append(item)

    def save(self, screen: pg.Surface):
        """Save a surface display"""
        self.pack(img.tostring(screen, COLOR_FORMAT))


if __name__ == "__main__":

    pg.init()
    screen = dis.set_mode(WIN_SIZE)
    screen.fill(WIN_BACK)
    dis.flip()

    # Infinite loop state
    run = True

    # Current tools parameters
    lst_pos: tuple = None
    color = DEFAULT_LINE_COLOR
    li_width = DEFAULT_LINE_WIDTH
    undo = Pile(MAX_UNDO)
    redo = Pile(MAX_REDO)

    while run:
        for ev in evh.get():  # Some spagettie code
            if ev.type == pg.QUIT:  # Cross clicked
                run = False
                break

            elif ev.type == pg.KEYDOWN:

                if ev.mod & pg.KMOD_LCTRL:  # If ctrl is down

                    if ev.key == pg.K_z:
                        if len(undo) > 0:
                            redo.save(screen)
                            im = img.fromstring(
                                undo.pop(), WIN_SIZE, COLOR_FORMAT)
                            screen.blit(im, im.get_rect())
                            dis.flip()

                    elif ev.key == pg.K_y:
                        if len(redo) > 0:
                            undo.save(screen)
                            im = img.fromstring(
                                redo.pop(), WIN_SIZE, COLOR_FORMAT)
                            screen.blit(im, im.get_rect())
                            dis.flip()

                    elif ev.key == pg.K_s:
                        fname = fd.asksaveasfilename(**FILE_DIALOG)
                        if fname:
                            img.save(screen, fname)

                    elif ev.key == pg.K_o:

                        # Open filename dialog and close it
                        fname = fd.askopenfilename(**FILE_DIALOG)

                        if fname:
                            undo.save(screen)
                            im = img.load(fname)
                            screen.blit(im, im.get_rect())
                            dis.flip()

                elif ev.key == pg.K_ESCAPE:
                    run = False
                    break

                else:
                    colo = KEY_MAP_COLOR.get(ev.unicode)
                    if colo:
                        color = colo

            elif ev.type == pg.MOUSEWHEEL:
                if ev.y > 0:
                    li_width += 1
                elif li_width > MIN_LI_WIDTH:
                    li_width -= 1

            elif ev.type == pg.MOUSEBUTTONDOWN:
                undo.save(screen)
                if ev.button == 1:
                    lst_pos = ev.pos
                elif ev.button == 3:
                    undo.save(screen)
                    screen.fill(color)
                    dis.flip()

            elif ev.type == pg.MOUSEBUTTONUP and ev.button == 1:
                lst_pos = None

            elif lst_pos and ev.type == pg.MOUSEMOTION:
                pg.draw.line(screen, color, lst_pos, ev.pos, li_width)
                lst_pos = ev.pos
                dis.flip()

    pg.quit()
    quit

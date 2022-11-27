# coding: utf-8
"""Main application module
"""


# Typing
from enum_ import *

# For interface
import tkyml as tky

# For story
from story import StoryRoot, StoryNode

# For relative path
import os


PATH_UI_FILE = "assets/window.yml"
PATH_STORY_FILE = "assets/story.yml"


@tky.register
class ImgButton(tky.WIDGETS.Img):

    """A special widget that act as a button but is an image
    """

    def __init__(self, *args: tuple[any]):
        super().__init__(*args)

        # Events

        @self.event(MouseEvent.ONPRESS)
        def _():
            self.set_class(Class.ACTIVE)

        @self.event(MouseEvent.ONRELEASE)
        def _():
            self.set_class(Class.UNACTIVE)

    def set_visibility(self, state: bool):
        """Change widget visibility

        Args:
            state (bool): Visible or not obviously
        """
        if state:
            self.set_class(Class.DEFAULT)
        else:
            self.set_class(Class.HIDE)


class App(tky.App):

    """Here is defined our app
    """

    snode: StoryNode  # Current sotry node
    rnode: StoryRoot  # Root story node
    i: int  # Current index in dialog
    undo: list[StoryNode]  # Undo node story pile
    redo: list[StoryNode]  # Redo node sotry pile

    name: tky.WIDGETS.Label  # Context text
    dialog: tky.WIDGETS.Label  # Dialog text
    next: tky.WIDGETS.Button  # Next / Quit button
    previous: tky.WIDGETS.Button  # Previous / Restart button
    top: ImgButton  # Top arrow button
    left: ImgButton  # Left arrow button
    right: ImgButton  # Right arrow button
    bottom: ImgButton  # Bottom arrow button

    def __init__(self):

        # Load UI
        super().__init__(PATH_UI_FILE)

        # Get all needed widgets
        self.name = self.nametowidget("main.name")
        self.dialog = self.nametowidget("main.dialog")
        self.next = self.nametowidget("main.button.next")
        self.previous = self.nametowidget("main.button.previous")
        self.top = self.nametowidget("top")
        self.left = self.nametowidget("left")
        self.right = self.nametowidget("right")
        self.bottom = self.nametowidget("bottom")

        # Set base attributes
        self.i = 0 
        self.undo = []
        self.redo = []

        # Set events
        self.set_events()

        # Load story
        self.rnode = StoryRoot(PATH_STORY_FILE)
        self.upd_snode(self.rnode)

        self.mainloop()

    def set_events(self):
        """Set events of app
        """
        @self.next.event(MouseEvent.ONCLICK, False)
        @self.event(KeyEvent.CTRL_MAJ_Z)
        def _():
            if self.i < len(self.snode.dialog) - 1:  # Navigate in dialog
                self.i += 1
                self.upd_dialog()
                self.upd_next()
            elif self.redo:  # Navigate in paths
                self.undo.append(self.snode)
                self.upd_snode(self.redo.pop())
                self.previous.set_class(Class.ACTIVE)
            else:
                if self.snode.end:
                    self.set_end()

        @self.previous.event(MouseEvent.ONCLICK, False)
        @self.event(KeyEvent.CTRL_Z)
        def _():
            if self.i > 0:  # Navigate in dialog
                self.i -= 1
                self.upd_dialog()
                self.next.set_class(Class.ACTIVE)
                if not self.undo and self.i == 0:
                    self.previous.set_class(Class.UNACTIVE)
            elif self.undo:  # Navigate in paths
                self.redo.append(self.snode)
                self.next.set_class(Class.ACTIVE)
                self.upd_snode(self.undo.pop())

        @self.top.event(MouseEvent.ONRELEASE)
        @self.event(KeyEvent.UP)
        def _():
            if self.snode.top:
                self.save_node()
                self.upd_snode(self.snode.top)

        @self.left.event(MouseEvent.ONRELEASE)
        @self.event(KeyEvent.LEFT)
        def _():
            if self.snode.left:
                self.save_node()
                self.upd_snode(self.snode.left)

        @self.right.event(MouseEvent.ONRELEASE)
        @self.event(KeyEvent.RIGHT)
        def _():
            if self.snode.right:
                self.save_node()
                self.upd_snode(self.snode.right)

        @self.bottom.event(MouseEvent.ONRELEASE)
        @self.event(KeyEvent.DOWN)
        def _():
            if self.snode.bottom:
                self.save_node()
                self.upd_snode(self.snode.bottom)

    def set_end(self):
        """Set end screen
        """
        # Update event
        for ev in KeyEvent:  # unbind all keyboard events
            self.unbind(ev)
        self.next.event(MouseEvent.ONCLICK, False)(self.destroy)  # Option quit
        self.previous.event(MouseEvent.ONCLICK, False)(
            self.reset)  # Option restart

        # Update UI
        self.name.configure(text='')
        self.dialog.configure(text=f"Game Over\n{self.snode.end}")
        self.dialog.set_class(Class.OVER)
        self.next.set_class(Class.OVER)
        self.previous.set_class(Class.OVER)

    def reset(self):
        self.dialog.set_class(Class.DEFAULT)
        self.next.set_class(Class.DEFAULT)
        self.previous.set_class(Class.DEFAULT)
        self.i = 0
        self.undo.clear()
        self.redo.clear()
        self.set_events()
        self.upd_snode(self.rnode)

    def save_node(self):
        self.undo.append(self.snode)
        self.redo.clear()

    def upd_name(self):
        """Update name
        """
        self.name.configure(text=self.snode.name)

    def upd_dialog(self):
        """Update dialog
        """
        self.dialog.configure(text=self.snode.dialog[self.i])

    def upd_next(self):
        """Update next button
        """
        if self.redo or self.i < len(self.snode.dialog) - 1 or self.snode.end:
            self.next.set_class(Class.ACTIVE)
        else:
            self.next.set_class(Class.UNACTIVE)

    def upd_snode(self, node: StoryNode):
        """Update story node

        Args:
            node (StoryNode): New StoryNode
        """
        self.snode = node
        self.i = 0
        self.upd_dialog()
        self.upd_name()
        self.upd_next()

        if self.undo:
            self.previous.set_class(Class.ACTIVE)
        else:
            self.previous.set_class(Class.UNACTIVE)

        self.top.set_visibility(node.top)
        self.left.set_visibility(node.left)
        self.right.set_visibility(node.right)
        self.bottom.set_visibility(node.bottom)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__)) # Avoid error with relative path if file is runned from outside
    App() # Start application

# coding: utf-8
"""Story tree module
"""

# Typing
from __future__ import annotations

# Tree / Node build
from dataclasses import dataclass
import yaml


# For yaml parser
ENCODING = "utf-8"
TAG_YML_MAP = "tag:yaml.org,2002:map"
TAG_YML_SEQ = "tag:yaml.org,2002:seq"


def __construct_sequence(loader, node):
    yield tuple(loader.construct_sequence(node))


yaml.add_constructor(TAG_YML_SEQ, __construct_sequence) # Load sequence as tuple (optimized)


@dataclass
class StoryNode:

    """A story node

    A story node with dialog, maybe a PNG, top/left/right/bottom paths end maybe an end. 
    """

    dialog: tuple
    name: str = ""

    top: StoryNode = None
    left: StoryNode = None
    right: StoryNode = None
    bottom: StoryNode = None

    end: str = None

    @classmethod
    def _from_yaml(cls, loader, node):
        yield cls(**loader.construct_mapping(node))


class StoryRoot(StoryNode):

    """The story root where we load the tree from a file
    """

    def __init__(self, file: str):
        with open(file, 'r', encoding=ENCODING) as file:
            yaml.add_constructor(TAG_YML_MAP, self._from_yaml)
            yaml.load(file, Loader=yaml.Loader)

    def _from_yaml(self, loader, node):
        yaml.add_constructor(TAG_YML_MAP, StoryNode._from_yaml)
        StoryNode.__init__(self, **loader.construct_mapping(node))

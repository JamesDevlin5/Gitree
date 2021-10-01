#!/usr/bin/env python3

import sys
from pathlib import PurePath


class Color:
    def __init__(self, code):
        self._code = code

    def __str__(self):
        return f"\033[{self.code}m"

    @property
    def code(self):
        return self._code


class BoldColor(Color):
    def __init__(self, code):
        super().__init__("1;" + code)


class ResetColor(Color):
    def __init__(self):
        super().__init__(0)


class Node:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class DirNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self._children = []

    @property
    def name(self):
        return super().name + "/"

    @property
    def children(self):
        return self._children

    def lookup(self, node):
        for item in self.children:
            if item.name == node.name:
                return item
        self.add_node(node)
        return node

    def add_node(self, node):
        self._children.append(node)

    def is_dir(self):
        return True


class FileNode(Node):
    def __init__(self, name, status):
        super().__init__(name)
        self._stat = status

    @property
    def status(self):
        return self._stat

    def is_dir(self):
        return False


class Status:
    def __init__(self, string):
        self._string = string

    def __str__(self):
        return self._string + ": "


class StatusEntry:
    def __init__(self, line):
        stat = line[0]
        path = line[3:]
        self._path = PurePath(path).parts
        self._stat = Status(stat)

    @property
    def status(self):
        return self._stat

    @property
    def dirs(self):
        return self._path[:-1]

    @property
    def filename(self):
        return self._path[-1]

    def to_dirnodes(self):
        return (DirNode(dir) for dir in self.dirs)

    def filenode(self):
        return FileNode(self.filename, self.status)


class StatusTree:
    def __init__(self):
        self._items = DirNode("")

    def add_entry(self, st_entry):
        parent = self._items
        for dirnode in st_entry.to_dirnodes():
            parent = parent.lookup(dirnode)
        parent.add_node(st_entry.filenode())

    def print_tree(self):
        def print_worker(prefix, items):
            for item in items[:-1]:
                if item.is_dir():
                    print(prefix + "├─ " + item.name)
                    print_worker(prefix + "│ ", item.children)
                else:
                    print(prefix + "├─ " + str(item.status) + item.name)
            if len(items) > 0:
                item = items[-1]
                if item.is_dir():
                    print(prefix + "└─ " + item.name)
                    print_worker(prefix + "  ", item.children)
                else:
                    print(prefix + "└─ " + str(item.status) + item.name)

        print_worker(prefix="", items=self._items.children)


tree = StatusTree()
for status in (StatusEntry(line) for line in sys.stdin.read().splitlines()):
    tree.add_entry(status)
tree.print_tree()

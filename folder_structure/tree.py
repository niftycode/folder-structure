#!/usr/bin/env python3

"""
generate_tree.py
This code is inspired by @realpython
https://realpython.com/directory-tree-generator-python/
Version: 1.0
Python 3.11+
Date created: January 18th, 2023
Date modified: January 19th, 2023
"""

import os
import pathlib
import logging


PIPE = '│'
ELBOW = '└──'
TEE = '├──'
PIPE_PREFIX = '│   '
SPACE_PREFIX = '    '


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FolderTree:
    """
    This class generates the folder structure.
    """

    def __init__(self, root_dir):
        self._generator = _TreeGenerator(root_dir)

    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


class _TreeGenerator:
    """
    This class builds the folder structure.
    The top level (_tree.head) is read first,
    then the subfolders (_tree.body) follow.
    """

    def __init__(self, root_dir):
        """
        Init method
        Args:
            root_dir: The root directory specified by the user
        """
        self._root_dir = pathlib.Path(root_dir)
        logger.debug(f'root_dir: {self._root_dir}')
        self._tree = []

    def build_tree(self):
        """
        Invoke _tree.head() and _tree.body() to build the complete tree and
        return the folder structure.
        Returns: The determined folder structure consisting of directories and files

        """
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        """
        Add the root directory and a PIPE to the _tree list.
        """
        self._tree.append(f'{self._root_dir}{os.sep}')
        self._tree.append(PIPE)

    def _tree_body(self, folder, prefix=''):
        """
        Iterate through the folder structure with iterdir().
        Invoke _add_directory() if it is a directory,
        otherwise invoke _add_file()
        Args:
            folder: The root directory.
            prefix: The prefix to use.
        """
        entries = folder.iterdir()
        entries = sorted(entries, key=lambda e: e.is_file())
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(
        self, directory, index, entries_count, prefix, connector
    ):
        """
        Add every directory to the _tree list.
        Args:
            directory: A discovered directory
            index: The index corresponding to the determined directory
            entries_count: Number of existing entries (directories, files)
            prefix: The prefix to use (for example a SPACE_PREFIX)
            connector: A PIPE or an ELBOW
        """
        self._tree.append(f'{prefix}{connector} {directory.name}{os.sep}')
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(folder=directory, prefix=prefix)
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        """
        Add every file to the _tree list.
        Args:
            file: A discovered file
            prefix: The prefix to use (for example a SPACE_PREFIX)
            connector: A PIPE or an ELBOW
        """
        self._tree.append(f'{prefix}{connector} {file.name}')

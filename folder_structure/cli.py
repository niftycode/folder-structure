#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
cli.py
This module provides the folder-structure CLI.
Version: 1.0
Python 3.11+
Date created: January 18th, 2023
Date modified: Janury 19th, 2023
"""

import argparse
import pathlib
import sys

from argparse import Namespace

from folder_structure import tree, info


def create_parser() -> argparse.ArgumentParser:
    """
    Create a command-line parser
    Returns: The created parser
    """
    parser = argparse.ArgumentParser(
        prog="folder-structure",
        description="This is folder-structure, a directory tree generator",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Show version and license",
    )

    parser.add_argument(
        "-d",
        "--directory",
        metavar="ROOT_DIR",
        default="",
        action="store",
        help="Generate a full directory tree starting at ROOT_DIR",
    )
    return parser


def evaluate_arguments(args: Namespace):
    """
    Evaluate the given argument
    Args:
        args: given arguments
    """
    if args.directory != "":
        root_dir = pathlib.Path(args.directory)
        if not root_dir.is_dir():
            print("The specified root directory doesn't exist")
            sys.exit()

        tree_structure = tree.FolderTree(root_dir)
        tree_structure.generate()

    if args.version:
        info.app_info()


def main():
    """
    The entry point of this program.
    """
    parser = create_parser()
    args = parser.parse_args()
    evaluate_arguments(args)


if __name__ == "__main__":
    main()

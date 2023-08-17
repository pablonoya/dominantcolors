#!/usr/bin/env python

import sys

from .dominantcolors import color_extractor


def main():
    """Extract dominant colors from image"""

    if len(sys.argv) != 2:
        print("Usage: python dominantcolor.py <path/to/image>")
        return

    image_path = sys.argv[1]
    color_extractor(image_path)


if __name__ == "main":
    main()

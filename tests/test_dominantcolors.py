import unittest
from unittest.mock import patch
from io import StringIO

from dominantcolors.cli import main as cli_main

from dominantcolors.dominantcolors import color_extractor


class TestDominantColors(unittest.TestCase):
    """Test dominantcolors.py"""

    def test_incorrect_cli_arguments(self):
        """Test that expected usage is printed"""
        captured_output = StringIO()
        with patch("sys.stdout", new=captured_output):
            cli_main()

        captured_output.seek(0)
        self.assertEqual(
            captured_output.read(), "Usage: python dominantcolor.py <path/to/image>\n"
        )

    def test_color_extractor(self):
        """Test that expected_colors are printed"""
        expected_colors = ["#913b24\n", "#d1ca9e\n", "#d16346\n"]

        captured_output = StringIO()
        with patch("sys.stdout", new=captured_output):
            color_extractor("tests/kodim02.png")

        captured_output.seek(0)
        self.assertEqual(captured_output.readlines(), expected_colors)


if __name__ == "__main__":
    unittest.main()

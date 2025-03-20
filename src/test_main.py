import unittest
from main import extract_title

class TestHtmlNode(unittest.TestCase):

    # Test EXTRACT TITLE H1
    
    def test_valid_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")
        self.assertEqual(extract_title("# Another title"), "Another title")

    def test_no_h1_title(self):
        with self.assertRaises(ValueError):
            extract_title("## Subtitle")
        with self.assertRaises(ValueError):
            extract_title("No hashtag")

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_only_hash_symbol(self):
        with self.assertRaises(ValueError):
            extract_title("#")
import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text nodes", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_URL_Difference(self):
        node1 = TextNode("Same text", TextType.LINK, "https://example.com")
        node2 = TextNode("Same text", TextType.LINK, "https://another-example.com")
        self.assertNotEqual(node1, node2)
        
    def test_different_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    
        


if __name__ == "__main__":
    unittest.main()
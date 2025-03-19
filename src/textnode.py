import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"      


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Invalid TextType")
    
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split('\n')
    if re.match(r'^#{1,6} .+', block.split('\n')[0]):
        return BlockType.HEADING
    
    if len(lines) >= 2 and lines[0].startswith('```') and lines[-1] == '```':
        return BlockType.CODE
    
    all_lines_are_quotes = all(line.startswith('>') for line in lines)
    if all_lines_are_quotes:
        return BlockType.QUOTE
    
    all_lines_are_unordered = all(line.startswith('- ') for line in lines)
    if all_lines_are_unordered:
        return BlockType.UNORDERED_LIST
    
    ordered = True
    for i in range(len(lines)):
        expected_prefix = f"{i+1}. "  # This creates "1. ", "2. ", etc.
        if not lines[i].startswith(expected_prefix):
            ordered = False
            break  # No need to check further if any line doesn't match
    if ordered and len(lines) > 0:  # Ensure we have at least one line
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
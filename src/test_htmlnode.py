import unittest

from htmlnode import *
from textnode import *
from textsplit import *

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_with_href(self):
        # Test with a simple href property
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_with_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://example.com", "target": "_blank"}
        )
        props_html = node.props_to_html()
        self.assertIn(' href="https://example.com"', props_html)
        self.assertIn(' target="_blank"', props_html)
        self.assertTrue(props_html.startswith(' '))

    def test_props_to_html_with_no_props(self):
        # Test with no properties
        node = HTMLNode("p", "Hello, world!", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://example.com", "class": "link"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" class="link">Click me!</a>')

    # PARENT NODE

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("span", "second")
        child3 = LeafNode("span", "third")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>first</span><span>second</span><span>third</span></div>"
        )

    def test_parent_node_with_props(self):
        child_node = LeafNode("span", "text")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>text</span></div>'
        )
    
    def test_complex_nested_structure(self):
        # Create a simple navigation menu
        menu_item1 = ParentNode("li", [LeafNode("a", "Home")])
        menu_item2 = ParentNode("li", [LeafNode("a", "About")])
        
        # The menu is a ul containing two list items
        menu = ParentNode("ul", [menu_item1, menu_item2])
        
        # A div containing a heading and the menu
        container = ParentNode("div", [
            LeafNode("h1", "My Site"),
            menu
        ])
        
        expected_html = "<div><h1>My Site</h1><ul><li><a>Home</a></li><li><a>About</a></li></ul></div>"
        
        self.assertEqual(container.to_html(), expected_html)

    # TEXT TO HTML NODE

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, {})

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, {})

    def test_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
        self.assertEqual(html_node.props, {})

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("An image description", TextType.IMAGE, url="https://image.url/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Image nodes have no value in HTML.
        self.assertEqual(html_node.props, {
            "src": "https://image.url/image.png",
            "alt": "An image description"
        })

    #TEXT SPLIT DELIMITER
    def test_single_delimiter_pair(self):
        # Test basic case with one pair of delimiters
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)
        self.assertEqual(result[1].text, expected[1].text)
        self.assertEqual(result[1].text_type, expected[1].text_type)
        self.assertEqual(result[2].text, expected[2].text)
        self.assertEqual(result[2].text_type, expected[2].text_type)

    def test_multiple_delimiter_pairs(self):
        # Test with multiple delimiter pairs
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 5)

    def test_basic_bold(self):
        # Test with a basic bold example
        node = TextNode("Hello **world**!", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "!")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_basic_italic(self):
        # Test with a basic italic example
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_no_delimiters(self):
        # Test with no delimiters in the text
        node = TextNode("Plain text only", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text only")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_multiple_bold_sections(self):
        # Test with multiple bold sections
        node = TextNode("This has **multiple** bold **sections**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "This has ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "multiple")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " bold ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "sections")
        self.assertEqual(result[3].text_type, TextType.BOLD)

    def test_basic_code(self):
        # Test with a single code block
        node = TextNode("Use the `print()` function", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Use the ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "print()")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " function")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_code_blocks(self):
        # Test with multiple code blocks
        node = TextNode("Functions like `len()` and `sum()` are built-in", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Functions like ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "len()")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "sum()")
        self.assertEqual(result[3].text_type, TextType.CODE)
        self.assertEqual(result[4].text, " are built-in")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    # TEST MARKDOWN REGEX (IMAGES + LINKS)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_alt_text(self):
        matches = extract_markdown_images("![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_markdown_images_special_characters(self):
        matches = extract_markdown_images("![hello @#$%](https://example.com/image.png)")
        self.assertListEqual([("hello @#$%", "https://example.com/image.png")], matches)

    def test_extract_markdown_links_parentheses_in_url(self):
        matches = extract_markdown_links("[link](https://example.com/path(1))")
        self.assertListEqual([("link", "https://example.com/path(1)")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("[link](https://example.com/path)")
        self.assertListEqual([("link", "https://example.com/path")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "![img1](https://img1.com) and ![img2](https://img2.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("img1", "https://img1.com"), ("img2", "https://img2.com")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "[first](https://first.com) and [second](https://second.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("first", "https://first.com"), ("second", "https://second.com")], matches)

    # SPLIT IMAGES AND LINKS

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just a normal sentence.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "Check out [Google](https://google.com) and [OpenAI](https://openai.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("OpenAI", TextType.LINK, "https://openai.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This is plain text.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_only_link(self):
        node = TextNode("[Just a link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Just a link", TextType.LINK, "https://example.com")
        ], new_nodes)

    def test_split_links_at_start_and_end(self):
        node = TextNode("[start](https://start.com) Middle text [end](https://end.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("start", TextType.LINK, "https://start.com"),
            TextNode(" Middle text ", TextType.TEXT),
            TextNode("end", TextType.LINK, "https://end.com"),
        ], new_nodes)

    def test_split_links_empty_display(self):
        node = TextNode("[](https://emptydisplay.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("", TextType.LINK, "https://emptydisplay.com")
        ], new_nodes)

    # TEXT TO TEXTNODE
    
    def test_text_to_textnode_default(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_node = text_to_textnodes(text)
        self.assertListEqual([
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ], text_node)

    def test_text_to_textnode_naruto(self):
        text = "Naruto is a **ninja** who loves his friends, especially Sasuke, who is his _rival_. Together, they fight against dangerous enemies like the `Akatsuki` and protect the village from evil. There’s also a picture of **Naruto** in his famous pose: ![Naruto pose](https://example.com/naruto.jpg) and a link to the village's website: [Hidden Leaf Village](https://naruto.com)."
        text_node = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("Naruto is a ", TextType.TEXT),
            TextNode("ninja", TextType.BOLD),
            TextNode(" who loves his friends, especially Sasuke, who is his ", TextType.TEXT),
            TextNode("rival", TextType.ITALIC),
            TextNode(". Together, they fight against dangerous enemies like the ", TextType.TEXT),
            TextNode("Akatsuki", TextType.CODE),
            TextNode(" and protect the village from evil. There’s also a picture of ", TextType.TEXT),
            TextNode("Naruto", TextType.BOLD),
            TextNode(" in his famous pose: ", TextType.TEXT),
            TextNode("Naruto pose", TextType.IMAGE, "https://example.com/naruto.jpg"),
            TextNode(" and a link to the village's website: ", TextType.TEXT),
            TextNode("Hidden Leaf Village", TextType.LINK, "https://naruto.com"),
            TextNode(".", TextType.TEXT),
            ], text_node)
        
    def test_text_to_textnode_darksouls(self):
        text = "In Dark Souls, **Estus Flask** is crucial for survival, while the _bonfire_ acts as a checkpoint. Watch out for the `boss fight` at the end, or you'll be doomed to repeat it forever!"
        text_node = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("In Dark Souls, ", TextType.TEXT),
            TextNode("Estus Flask", TextType.BOLD),
            TextNode(" is crucial for survival, while the ", TextType.TEXT),
            TextNode("bonfire", TextType.ITALIC),
            TextNode(" acts as a checkpoint. Watch out for the ", TextType.TEXT),
            TextNode("boss fight", TextType.CODE),
            TextNode(" at the end, or you'll be doomed to repeat it forever!", TextType.TEXT),
        ], text_node)
        

    # TEST MARKDOWN TO BLOCKS
    
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_multiple_blank_lines(self):
        md = "Paragraph one\n\n\n\nParagraph two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph one", "Paragraph two"])

    def test_leading_trailing_whitespace(self):
        md = "\n\n   Paragraph with whitespace   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph with whitespace"])

    def test_only_whitespace(self):
        md = "   \n\n \t \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_complex_markdown(self):
        md = """
        Here is some text.

        - List item one with `code`
        - List item two

            ```
            block code here
            still block code
            ```

        Another paragraph.
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Here is some text.",
            "- List item one with `code`\n- List item two",
            "```\nblock code here\nstill block code\n```",
            "Another paragraph."
        ])

    def test_headers(self):
        md = "# Header 1\n\nParagraph under header\n\n## Header 2\nMore text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "# Header 1",
            "Paragraph under header",
            "## Header 2\nMore text"
        ])

    def test_markdown_with_excessive_newlines(self):
        md = """


        Paragraph after excessive newlines.


        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Paragraph after excessive newlines."
        ])

    # BLOCK TO BLOCK TYPE

    def test_heading_block(self):
        block = "# Heading Level 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "### Heading Level 3\nMore text"  # Still heading (only checks first line)
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "Not a heading"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ndef function():\n    pass\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "```\nIncomplete code block"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote_block(self):
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "> Quote\nNormal line"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "- Item 1\nNot an item"
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "1. First\n3. Skipped number"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "1. Only one item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "Just a simple paragraph without markdown."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "Random text\nSecond line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "-Incorrect markdown item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_edge_block_cases(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "###### Heading level 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "####### Invalid heading (7 hashes)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "-Not actually list (no space after -)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "1.First item without space after dot"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # MK BLOCKS TO HTML
    
    def test_mk_paragraphs_to_html(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_mk_codeblock_to_html(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_mk_paragraph_to_html_naruto(self):
        md = """
        Naruto said, **"I never go back on my word!"** That's my _nindō_, my ninja way!

        Sasuke replied coldly, `"You're still such a loser, Naruto."`
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Naruto said, <b>\"I never go back on my word!\"</b> That's my <i>nindō</i>, my ninja way!</p><p>Sasuke replied coldly, <code>\"You're still such a loser, Naruto.\"</code></p></div>",
        )

    def test_mk_codeblock_to_html_with_bleach_dialogue(self):
        md = """
        ```
        Ichigo: Bankai!
        Byakuya: Impossible... his speed has **increased**!
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>Ichigo: Bankai!\nByakuya: Impossible... his speed has **increased**!\n</code></pre></div>",
        )

    def test_mk_heading_to_html_with_anime(self):
        md = """
        # Naruto's Dream
        ## Hokage Journey
        ### Shadow Clone Techniques
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Naruto's Dream</h1><h2>Hokage Journey</h2><h3>Shadow Clone Techniques</h3></div>",
        )

    def test_mk_quote_to_html_with_bleach_philosophy(self):
        md = """
        > If miracles only happen once, what are they called the second time?
        > – Ichigo Kurosaki
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>If miracles only happen once, what are they called the second time?\n– Ichigo Kurosaki</blockquote></div>",
        )

    def test_mk_unordered_list_to_html_jutsu(self):
        md = """
        - **Chidori**
        - _Amaterasu_
        - `Susano'o`
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>Chidori</b></li><li><i>Amaterasu</i></li><li><code>Susano'o</code></li></ul></div>",
        )

    def test_mk_ordered_list_to_html_bleach_characters(self):
        md = """
        1. Ichigo Kurosaki
        2. Rukia Kuchiki
        3. Kisuke Urahara
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Ichigo Kurosaki</li><li>Rukia Kuchiki</li><li>Kisuke Urahara</li></ol></div>",
        )



    

if __name__ == "__main__":
    unittest.main()
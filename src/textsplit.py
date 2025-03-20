from textnode import *
from htmlnode import *


# old_notes = list
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            results.append(old_node)
        else:
            # Split by the delimiter - this gives us pieces with and without the delimiter
            parts = old_node.text.split(delimiter)
            
            # If we only have one part, there were no delimiters
            if len(parts) == 1:
                results.append(old_node)
                continue
                
            # If we have an odd number of parts, we have an equal number of opening and closing delimiters
            if len(parts) % 2 == 0:
                raise Exception(f"No closing delimiter '{delimiter}' found")
                
            current_nodes = []
            
            # Process each part
            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                    
                # Even indexes (0, 2, 4...) are outside delimiters (regular text)
                # Odd indexes (1, 3, 5...) are inside delimiters (formatted text)
                if i % 2 == 0:
                    current_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    current_nodes.append(TextNode(parts[i], text_type))
            
            results.extend(current_nodes)

    return results

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        
        if not images:
            result.append(old_node)
            continue
        
        remaining_text = old_node.text

        for image_alt, path in images:
            markdown_image = f"![{image_alt}]({path})"
            
            parts = remaining_text.split(markdown_image, 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            
            result.append(TextNode(image_alt, TextType.IMAGE, path))
            
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
        
    return result





def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)

        if not links:
            result.append(old_node)
            continue
        
        remaining_text = old_node.text

        for link_text, url in links:
            markdown_link = f"[{link_text}]({url})"
            
            parts = remaining_text.split(markdown_link, 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            
            result.append(TextNode(link_text, TextType.LINK, url))
            
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
        
    return result



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # for node in nodes:
    #     print(node)
    return nodes

def markdown_to_blocks(markdown):
    # Split the string into lines
    lines = markdown.split('\n')
    
    # Combine lines into blocks
    blocks = []
    current_block = []
    
    for line in lines:
        # Strip the line to handle indentation
        cleaned_line = line.strip()
        
        if cleaned_line:
            # If the line is not empty, add it to the current block
            current_block.append(cleaned_line)
        elif current_block:
            # If the line is empty and we have a current block, finish it
            blocks.append("\n".join(current_block))
            current_block = []
    
    # Don't forget the last block if it exists
    if current_block:
        blocks.append("\n".join(current_block))
    
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = HTMLNode(tag="div", children=[])
    
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type.value == "paragraph":
            # Create the paragraph node
            paragraph_node = HTMLNode(tag="p", children=[])

            # Replace newlines with spaces and normalize whitespace

            normalized_text = re.sub(r'\s+', ' ', block.replace('\n', ' ')).strip()

            # Process the paragraph text and assign the children
            paragraph_node.children = text_to_children(normalized_text)

            # Add the paragraph node to the parent
            parent_node.children.append(paragraph_node)

        elif block_type.value == "heading":
            # Split the block into lines to handle multiple headings
            lines = block.split("\n")
            for line in lines:
                if line.strip():  # Only process non-empty lines
                    heading_match = re.match(r'^(#+)', line)
                    if heading_match:
                        heading_level = len(heading_match.group(1))
                        
                        # Create the heading node
                        heading_node = HTMLNode(tag=f"h{heading_level}", children=[])

                        # Remove the heading markers and any leading/trailing whitespaces
                        heading_text = line[heading_level:].strip()

                        # Process the heading text and assign the children
                        heading_node.children = text_to_children(heading_text)

                        # Add the heading node to the parent
                        parent_node.children.append(heading_node)

        elif block_type.value == "code":
            # Create the code node structure: pre > code
            code_node = HTMLNode(tag="code", children=[])
            pre_node = HTMLNode(tag="pre", children=[code_node])
            
            # Extract the code content from the block
            code_content = block.strip()
            if code_content.startswith("```") and code_content.endswith("```"):
                code_content = code_content[3:-3]

            # To make sure the code content has a trailing newline
            code_content = code_content.lstrip("\n")

            # Ensure exactly one trailing newline
            code_content = code_content.rstrip("\n") + "\n"

            # Create a text node with type "text" to avoid inline markdown processing
            text_node = TextNode(code_content, TextType.TEXT)

            # Convert to HTML node and add as child to code_node
            code_node.children.append(text_node_to_html_node(text_node))

            # Add pre_node to parent
            parent_node.children.append(pre_node)
            
        
        elif block_type.value == "quote":
            # Remove the '>' marker from each line and join them
            quote_lines = [line.lstrip('>').strip() for line in block.split('\n')]
            quote_content = '\n'.join(quote_lines).strip()

            # Create the blockquote node
            blockquote_node = HTMLNode(tag="blockquote", children=[])

            # Process the quote content and assign children
            blockquote_node.children = text_to_children(quote_content)

            #Add to parent
            parent_node.children.append(blockquote_node)
            
        elif block_type.value == "unordered_list":
            # Create the ul node
            ul_node = HTMLNode(tag="ul", children=[])
            
            # Split the block into lines (list items)
            list_items = block.split("\n")

            # Process each list item
            for item in list_items:
                if item.strip():
                    # Remove the '- ' prefix and trim
                    item_text = item.strip().lstrip('-').strip()

                    # Create a list item node
                    li_node = HTMLNode(tag="li", children=[])

                    # Process inline formatting for the item text
                    li_node.children = text_to_children(item_text)

                    # Add the list item to the unordered list
                    ul_node.children.append(li_node)
            
            # Add the list item to the unordered list
            parent_node.children.append(ul_node)

        elif block_type.value == "ordered_list":
            # Create the ol node
            ol_node = HTMLNode(tag="ol", children=[])
            
            # Split the block into lines (list items)
            list_items = block.split("\n")

            # Process each list item
            for item in list_items:
                if item.strip(): #Skip empty lines
                    # Remove the number prefix using regex
                    item_text = re.sub(r'^\d+\.\s*', '', item.strip())

                    # Create a list item node
                    li_node = HTMLNode(tag="li", children=[])

                    # Process inline formatting for the item text
                    li_node.children = text_to_children(item_text)

                    # Add the list item to the unordered list
                    ol_node.children.append(li_node)
            
            # Add the list item to the unordered list
            parent_node.children.append(ol_node)

    return parent_node

        

        # if block_type == "paragraph":

def text_to_children(text):
    # Convert the text to a list of TextNodes (my function)
    text_nodes = text_to_textnodes(text)

    # Convert each TextNode to an HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes
    
# markdown_text ="- This is the first list item in a list block\n\n- This is a list item\n\n- This is another list item"

# print(markdown_to_html_node(markdown_text))



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
            paragraph_node = HTMLNode(tag="p", children=[])
            paragraph_node.children = text_to_children(block)
            parent_node.children.append(paragraph_node)

        elif block_type.value == "heading":
            heading_match = re.match(r'^(#+)', block)
            if heading_match:
                heading_level = len(heading_match.group(1))
                
                # Create the heading node
                heading_node = HTMLNode(tag=f"h{heading_level}", children=[])

                # Remove the heading markers and any leading/trailing whitespaces
                heading_text = block[heading_level:].strip()

                # Process the heading text and assign the children
                heading_node.children = text_to_children(heading_text)

                # Add the heading node to the parent
                parent_node.children.append(heading_node)

        elif block_type.value == "code":
            # Remove the triple backticks and get the code content
            code_content = "\n".join(block.split("\n")[1:-1]) # Skip first and last lines with ```

            # Create the pre and code nodes
            pre_node = HTMLNode(tag="pre", children=[])
            code_node = HTMLNode(tag="code", children=[])

            # TextNode directly
            text_node = TextNode(code_content)
            code_html_node = text_node_to_html_node(text_node)

            # Build the nested structure: pre > code > content
            code_node.children = [code_html_node]
            pre_node.children = [code_node]

            # Add to parent
            parent_node.children.append(pre_node)
            
            
        elif block_type.value == "quote":
            content = block.split()[2:-1]

            pre_block_quote = 
            
        elif block_type.value == "unordered_list":
            # Create ul node with li children
            
        elif block_type.value == "ordered_list":
            # Create ol node with li children

        

        # if block_type == "paragraph":

    


    
    
markdown_text ="- This is the first list item in a list block\n\n- This is a list item\n\n- This is another list item"

print(markdown_to_html_node(markdown_text))



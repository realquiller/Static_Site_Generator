import re

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
            if self.props is None or len(self.props) == 0:
                return ""
            return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        print(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("A LeafNode must have a value.")  # Ensure value is always given
        super().__init__(tag, value, None, props or {})  # Default props to an empty dict if None

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return str(self.value)

        # Build the attributes string, if any
        attributes = " ".join(f'{key}="{value}"' for key, value in self.props.items())

        # Create the opening tag with attributes, if attributes exist
        opening_tag = f"<{self.tag}{(' ' + attributes) if attributes else ''}>"

        # Combine the opening tag, value, and closing tag
        return f"{opening_tag}{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("A ParentNode must have a tag.")
        elif self.children is None:
            raise ValueError("A ParentNode must have children.")
        else:
            children_html = "".join(child.to_html() for child in self.children)
            attributes = self.props_to_html()
            return f"<{self.tag}{attributes}>{children_html}</{self.tag}>"
        

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?\)?)\)", text)




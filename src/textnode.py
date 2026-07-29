from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(text_node) -> LeafNode:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        elif text_node.text_type == TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode(tag="img", value='', props={"src": text_node.url, "alt": text_node.text})
        else:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Splits a list of TextNode objects into multiple TextNode objects based on a delimiter.

    Args:
        old_nodes (list[TextNode]): The list of TextNode objects to be split.
        delimiter (str): The delimiter to split the text on.
        text_type (TextType): The type of the resulting TextNode objects.

    Returns:
        list[TextNode]: A new list of TextNode objects after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extracts markdown image syntax from a given text.

    Args:
        text (str): The input text containing markdown image syntax.

    Returns:
        list[tuple[str, str]]: A list of tuples containing the image alt text and source URL.
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extracts markdown link syntax from a given text.

    Args:
        text (str): The input text containing markdown link syntax.
    Returns:
        list[tuple[str, str]]: A list of tuples containing the link text and URL.
    """
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits a list of TextNode objects into multiple TextNode objects based on markdown image syntax.

    Args:
        old_nodes (list[TextNode]): The list of TextNode objects to be split.

    Returns:
        list[TextNode]: A new list of TextNode objects after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for match in matches:
            alt_text, url = match
            start_index = node.text.find(f"![{alt_text}]({url})", last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = start_index + len(f"![{alt_text}]({url})")

        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits a list of TextNode objects into multiple TextNode objects based on markdown link syntax.

    Args:
        old_nodes (list[TextNode]): The list of TextNode objects to be split.

    Returns:
        list[TextNode]: A new list of TextNode objects after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0
        for match in matches:
            link_text, url = match
            start_index = node.text.find(f"[{link_text}]({url})", last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_index = start_index + len(f"[{link_text}]({url})")

        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts a string of text into a list of TextNode objects.

    Args:
        text (str): The input text to be converted.

    Returns:
        list[TextNode]: A list of TextNode objects representing the input text.
    """
    node = TextNode(text, TextType.TEXT)
        
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    for node in new_nodes:
        if node.text_type == TextType.TEXT and node.text.strip() == "":
            new_nodes.remove(node)
    return new_nodes
    
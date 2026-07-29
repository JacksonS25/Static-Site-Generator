from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_blocks
from textnode import TextType, TextNode, split_nodes_image, split_nodes_link, split_nodes_delimiter, text_to_textnodes
from blocktype import BlockType, block_to_block_type
import re

def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Converts a markdown string to an HTMLNode.

    Args:
        markdown (str): The markdown string to be converted.

    Returns:
        HTMLNode: The resulting HTMLNode.
    """
    blocks = markdown_to_blocks(markdown)

    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            # Assuming the heading level is determined by the number of '#' characters
            text_nodes = text_to_textnodes(block.strip('# '))
            level = len(block.split(' ')[0])  # Count '#' characters
            children.append(ParentNode(tag=f"h{level}", children=[node.text_node_to_html_node() for node in text_nodes]))
        elif block_type == BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block.replace("\n", " "))
            children.append(ParentNode(tag="p", children=[node.text_node_to_html_node() for node in text_nodes]))
        elif block_type == BlockType.ORDERED_LIST:
            list_items = [re.sub(r"\d\.", "", item).strip() for item in block.split('\n') if item.strip()]
            list_children = [ParentNode(tag="li", children=[node.text_node_to_html_node() for node in text_to_textnodes(item)]) for item in list_items]
            children.append(ParentNode(tag="ol", children=list_children))
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = [item.strip("- ").strip() for item in block.split('\n') if item.strip()]
            list_children = [ParentNode(tag="li", children=[node.text_node_to_html_node() for node in text_to_textnodes(item)]) for item in list_items]
            children.append(ParentNode(tag="ul", children=list_children))
        elif block_type == BlockType.CODE:
            block = block.strip("```\n")
            children.append(ParentNode(tag="pre", children=[LeafNode(tag="code", value=f"{block}\n")]))
        elif block_type == BlockType.QUOTE:
            stripped_block = block.replace("> ", "").replace(">\n", "")
            children.append(ParentNode(tag="blockquote", children=[node.text_node_to_html_node() for node in text_to_textnodes(stripped_block)]))
        

        
        # Add more block types as needed

    return ParentNode("div", children)
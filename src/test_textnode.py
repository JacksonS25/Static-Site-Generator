import unittest
from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_texttype_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, url="https://example.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_split_node_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_node_delimiter_multiple(self):
        node = TextNode("This is text with a `code block` and another `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "code block")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
    
    def test_split_node_delimiter_no_delimiter(self):
        node = TextNode("This is text with no code block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with no code block")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_split_node_delimiter_odd_parts(self):
        node = TextNode("This is text with a `code block` and another `code block` and one more `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "code block")
        self.assertEqual(new_nodes[4].text, " and one more ")
        self.assertEqual(new_nodes[5].text, "code block")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text_type, TextType.CODE)
    
    def test_split_node_delimiter_with_delimiter_at_start(self):
        node = TextNode("`code block` and some text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "code block")
        self.assertEqual(new_nodes[1].text, " and some text")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
    
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
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )
    
    def test_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_text_to_textnodes_with_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(len(text_nodes), 10)
        self.assertEqual(text_nodes[0].text, "This is ")
        self.assertEqual(text_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(text_nodes[1].text, "text")
        self.assertEqual(text_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(text_nodes[2].text, " with an ")
        self.assertEqual(text_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(text_nodes[3].text, "italic")
        self.assertEqual(text_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(text_nodes[4].text, " word and a ")
        self.assertEqual(text_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(text_nodes[5].text, "code block")
        self.assertEqual(text_nodes[5].text_type, TextType.CODE)
        self.assertEqual(text_nodes[6].text, " and an ")
        self.assertEqual(text_nodes[6].text_type, TextType.TEXT)
        self.assertEqual(text_nodes[7].text, "obi wan image")
        self.assertEqual(text_nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(text_nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(text_nodes[8].text, " and a ")
        self.assertEqual(text_nodes[8].text_type, TextType.TEXT)
        self.assertEqual(text_nodes[9].text, "link")
        self.assertEqual(text_nodes[9].text_type, TextType.LINK)
        self.assertEqual(text_nodes[9].url, "https://boot.dev")
    
    def test_text_to_textnodes_with_no_special_types(self):
        text = "This is a simple text with no special types."
        text_nodes = text_to_textnodes(text)
        self.assertEqual(len(text_nodes), 1)
        self.assertEqual(text_nodes[0].text, text)
        self.assertEqual(text_nodes[0].text_type, TextType.TEXT)
    
    def test_text_to_textnodes_with_only_special_types(self):
        text = "**Bold** _Italic_ `Code` ![Image](https://example.com/image.png) [Link](https://example.com)"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(len(text_nodes), 5)
        self.assertEqual(text_nodes[0].text, "Bold")
        self.assertEqual(text_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(text_nodes[1].text, "Italic")
        self.assertEqual(text_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(text_nodes[2].text, "Code")
        self.assertEqual(text_nodes[2].text_type, TextType.CODE)
        self.assertEqual(text_nodes[3].text, "Image")
        self.assertEqual(text_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(text_nodes[3].url, "https://example.com/image.png")
        self.assertEqual(text_nodes[4].text, "Link")
        self.assertEqual(text_nodes[4].text_type, TextType.LINK)
        self.assertEqual(text_nodes[4].url, "https://example.com")

if __name__ == "__main__":
    unittest.main()
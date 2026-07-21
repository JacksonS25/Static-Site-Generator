import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        expected_html = 'class="container" id="main"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_without_props(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "container"})
        expected_repr = "HTMLNode(tag=div, value=Hello, children=[], props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()

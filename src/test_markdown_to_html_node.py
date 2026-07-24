import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)

        html = node.to_html()

        self.assertEqual(html, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
    
    def test_paragraphs(self):
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
    
    def test_headings(self):
        md = """
# Heading 1

## Heading 2

```
### Heading 3
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><pre><code>### Heading 3\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- Item 1
- Item 2

```
- Item 3
```

1. Ordered 1
2. Ordered 2

```
1. Ordered 3
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li></ul><pre><code>- Item 3\n</code></pre><ol><li>Ordered 1</li><li>Ordered 2</li></ol><pre><code>1. Ordered 3\n</code></pre></div>",
        )
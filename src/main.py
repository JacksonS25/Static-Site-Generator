from textnode import TextNode, TextType


def main():
    new_node = TextNode("Hello, World!", TextType.PLAIN)
    print(new_node)


if __name__ == '__main__':
    main()
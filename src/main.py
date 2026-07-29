from static_to_public import copy_static_to_public
from generate_page import generate_pages_recursive
import sys

def main():
    base_path = sys.argv[1]
    static_dir = "static"
    public_dir = "docs"
    copy_static_to_public(static_dir, public_dir)
    generate_pages_recursive("content", "template.html", "docs", base_path)

if __name__ == '__main__':
    main()
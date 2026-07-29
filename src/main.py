from static_to_public import copy_static_to_public
from generate_page import generate_pages_recursive

def main():
    static_dir = "static"
    public_dir = "public"
    copy_static_to_public(static_dir, public_dir)
    generate_pages_recursive("content", "template.html", "public")

if __name__ == '__main__':
    main()
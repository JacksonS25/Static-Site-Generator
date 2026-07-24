from static_to_public import copy_static_to_public
from generate_page import generate_page

def main():
    static_dir = "static"
    public_dir = "public"
    copy_static_to_public(static_dir, public_dir)
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == '__main__':
    main()
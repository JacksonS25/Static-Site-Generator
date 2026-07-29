from markdown_to_html_node import markdown_to_html_node
import htmlnode
import os
from pathlib import Path

def generate_page(from_path, template_path, dest_path):
    """
    Generates a page by reading content from a source file, applying a template, and writing the result to a destination file.

    Args:
        from_path (str): The path to the source content file.
        template_path (str): The path to the HTML template file.
        dest_path (str): The path where the generated page will be saved.
    """
    print(f"Generating page from {from_path} to {dest_path} using template: {template_path}")

    # Read the content from the source file
    with open(from_path, "r") as f:
        content = f.read()

    # Read the template file
    with open(template_path, "r") as f:
        template = f.read()

    # Convert the markdown content to an HTMLNode
    html_node = markdown_to_html_node(content)
    html = html_node.to_html()
    title = htmlnode.extract_title(content)
    # Apply the template
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Write the generated HTML to the destination file
    file_path = Path(dest_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    list_of_contents = os.listdir(dir_path_content)
    for content in list_of_contents:
        if os.path.isfile(f"{dir_path_content}/{content}"):
            generate_page(f"{dir_path_content}/{content}", template_path, f"{dest_dir_path}/{content.strip(".md")}.html")
        else:
            generate_pages_recursive(f"{dir_path_content}/{content}", template_path, f"{dest_dir_path}/{content}")

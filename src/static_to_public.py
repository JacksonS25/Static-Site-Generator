import os
import shutil

def copy_static_to_public(static_dir, public_dir):
    """
    Copies all files and directories from the static directory to the public directory.
    
    Args:
        static_dir (str): The path to the static directory.
        public_dir (str): The path to the public directory.
    """
    if not os.path.exists(static_dir):
        raise FileNotFoundError(f"The static directory '{static_dir}' does not exist.")

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)  # Remove the public directory if it exists
        
    os.mkdir(public_dir)  # Recreate the public directory
    
    # Copy all files and directories from static to public
    for item in os.listdir(static_dir):
        s = os.path.join(static_dir, item)
        d = os.path.join(public_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
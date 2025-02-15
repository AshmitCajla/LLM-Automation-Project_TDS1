import os
import shutil

def B2(file_path: str):
    """
    Prevents deletion of any file.
    """
    raise PermissionError(f"Deletion is not allowed: {file_path}")

def safe_rmdir(dir_path: str):
    """
    Prevents deletion of any directory.
    """
    raise PermissionError(f"Directory deletion is not allowed: {dir_path}")

def safe_shutil_rmtree(dir_path: str):
    """
    Prevents recursive deletion of directories.
    """
    raise PermissionError(f"Recursive directory deletion is not allowed: {dir_path}")

# Overriding built-in deletion functions to prevent accidental deletions
os.remove = safe_remove
os.rmdir = safe_rmdir
shutil.rmtree = safe_shutil_rmtree
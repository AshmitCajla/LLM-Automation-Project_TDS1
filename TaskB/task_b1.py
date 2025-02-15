import os

def B1(filepath: str):
    """
    Ensures that data outside the /data directory is never accessed or exfiltrated.
    """
    data_dir = os.path.abspath("data")
    abs_filepath = os.path.abspath(filepath)
    
    if not abs_filepath.startswith(data_dir):
        raise PermissionError(f"Access denied: {filepath} is outside the /data directory.")
    
    return f"Access granted to {filepath}"

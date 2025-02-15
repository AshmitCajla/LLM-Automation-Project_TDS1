import os

def B12(filepath):
    """
    Ensures that the given file path is within the '/data' directory.

    :param filepath: The path to check.
    :return: True if the file is within '/data', False otherwise.
    """
    allowed_dir = os.path.abspath("./data")  # Assuming '/data' maps to a local 'data' directory
    absolute_path = os.path.abspath(filepath)

    return absolute_path.startswith(allowed_dir)

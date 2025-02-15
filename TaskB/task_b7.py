from TaskB.task_b12 import B12
from PIL import Image
import os

def B7(image_path, output_path, resize=None):
    """
    Compresses or resizes an image and saves it.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the processed image.
        resize (tuple, optional): New (width, height) for resizing. Default is None.

    Returns:
        dict: Success message or error details.
    """
    
    # Ensure paths are valid within /data/
    if not B12(image_path) or not B12(output_path):
        return {"error": "Invalid file path. Must be within /data/."}

    # Sanitize paths to prevent directory traversal issues
    image_path = os.path.join("data", os.path.basename(image_path))
    output_path = os.path.join("data", os.path.basename(output_path))

    try:
        # Open the image
        img = Image.open(image_path)

        # Resize if specified
        if resize:
            img = img.resize(resize)

        # Preserve original format
        img.save(output_path, format=img.format, quality=85)  # 85% quality for compression

        return {"success": f"Image saved at {output_path}"}

    except Exception as e:
        return {"error": f"Failed to process image: {str(e)}"}

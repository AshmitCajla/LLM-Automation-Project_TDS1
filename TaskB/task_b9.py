from TaskB.task_b12 import B12
import markdown
import os

def B9(md_path, output_path):
    """
    Converts a Markdown file to HTML and saves the output.

    Args:
        md_path (str): Path to the input Markdown file.
        output_path (str): Path to save the converted HTML.

    Returns:
        dict: Success message or error details.
    """

    # Ensure paths are valid within /data/
    if not B12(md_path) or not B12(output_path):
        return {"error": "Invalid file path. Must be within /data/."}

    # Prevent directory traversal by sanitizing paths
    md_path = os.path.join("data", os.path.basename(md_path))
    output_path = os.path.join("data", os.path.basename(output_path))

    try:
        # Read the Markdown file
        with open(md_path, "r", encoding="utf-8") as file:
            md_content = file.read()

        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content)

        # Save the converted HTML
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        return {"success": f"Markdown converted and saved at {output_path}"}

    except FileNotFoundError:
        return {"error": f"Markdown file '{md_path}' not found."}
    except Exception as e:
        return {"error": f"Failed to convert Markdown: {str(e)}"}

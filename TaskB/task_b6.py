import requests
from TaskB.task_b12 import B12
import os

def B6(url, output_filename):
    """
    Scrapes a webpage and saves the HTML content to a file.

    Args:
        url (str): The URL of the webpage to scrape.
        output_filename (str): Path to save the scraped content.

    Returns:
        str: The scraped HTML content or an error message.
    """

    # Ensure output file is within allowed directory
    if not B12(output_filename):
        return {"error": "Invalid output file path. Must be within /data/."}

    # Remove leading slashes for security
    output_filename = os.path.join("data", os.path.basename(output_filename))

    try:
        # Fetch the web page
        response = requests.get(url, timeout=10)  # 10s timeout
        response.raise_for_status()  # Raise an error for HTTP errors (4xx, 5xx)

        # Save content to a file
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(response.text)

        return response.text

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch webpage: {str(e)}"}

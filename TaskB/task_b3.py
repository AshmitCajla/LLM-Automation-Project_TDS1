import requests
import os
from TaskB.task_b12 import B12

def B3(url, save_path):
    """
    Fetch data from an API and save it to a file.
    
    Args:
        url (str): The API endpoint to fetch data from.
        save_path (str): The file path where data should be saved (must be inside /data/).
    
    Returns:
        dict: Result message and status.
    """
    # Ensure the save path is valid
    if not B12(save_path):
        return {"error": "Invalid save path. Data must be stored within /data/."}

    # Enforce relative path to prevent directory traversal attacks
    save_path = os.path.join("data", os.path.basename(save_path))

    try:
        response = requests.get(url, timeout=10)  # Timeout to avoid hanging requests
        if response.status_code != 200:
            return {"error": f"Failed to fetch data: HTTP {response.status_code}"}
        
        # Save to file
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)

        return {"success": f"Data saved to {save_path}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

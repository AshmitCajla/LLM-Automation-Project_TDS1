import subprocess
import os
from datetime import datetime
from TaskB.task_b12 import B12

def B4(repo_url, save_path, commit_message="Automated commit"):
    """
    Clone a Git repository and make a commit.
    
    Args:
        repo_url (str): The URL of the Git repository.
        save_path (str): The directory where the repo should be cloned (must be inside /data/).
        commit_message (str): The commit message for changes.

    Returns:
        dict: Success or error message.
    """

    # Ensure save_path is valid and within /data/
    if not B12(save_path):
        return {"error": "Invalid save path. Repository must be stored within /data/."}

    save_path = os.path.join("data", os.path.basename(save_path))  # Ensure safe path

    try:
        # Clone the repository
        if not os.path.exists(save_path):
            subprocess.run(["git", "clone", repo_url, save_path], check=True)
        else:
            return {"error": "Repository already exists at the specified location."}

        # Create a new file to simulate changes
        file_path = os.path.join(save_path, "autocommit.txt")
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"Automated commit at {datetime.now()}\n")

        # Commit changes
        subprocess.run(["git", "-C", save_path, "add", "."], check=True)
        subprocess.run(["git", "-C", save_path, "commit", "-m", commit_message], check=True)

        return {"success": f"Repository cloned and committed at {save_path}"}

    except subprocess.CalledProcessError as e:
        return {"error": f"Git command failed: {e}"}

    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

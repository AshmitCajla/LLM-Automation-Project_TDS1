from dotenv import load_dotenv
import os
import requests
import json

def load_api_token():
    """Load the OpenAI API token from environment variables."""
    load_dotenv()
    api_token = os.getenv("OPENAI_API_KEY")
    if not api_token:
        raise RuntimeError("API token not found in environment variables. Make sure to set OPENAI_API_KEY.")
    return api_token

def determine_task(task_description: str):
    """
    Map a task description to a predefined canonical task and extract the script URL if applicable.
    Returns a tuple (task_id, url), where url is non-empty only for task A1.
    """
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    api_token = load_api_token()
    
    system_prompt = (
        "You are an assistant that maps a given task description to one of the following canonical tasks:\n\n"
        "A1: Install uv (if required) and run the datagen script from URL with the user's email as an argument.\n"
        "A2: Format the contents of /data/format.md using prettier@3.4.2, updating the file in-place.\n"
        "A3: Count the number of a specific weekday in a file and write the count to an output file.\n"
        "A4: Sort contacts from /data/contacts.json and save to /data/contacts-sorted.json.\n"
        "A5: Extract first lines from the 10 most recent .log files and save to /data/logs-recent.txt.\n"
        "A6: Index Markdown titles in /data/docs/ and save to /data/docs/index.json.\n"
        "A7: Extract sender’s email from /data/email.txt and save to /data/email-sender.txt.\n"
        "A8: Extract credit card number from /data/credit-card.png and save to /data/credit-card.txt.\n"
        "A9: Find the most similar pair of comments in /data/comments.txt and save them.\n"
        "A10: Compute total sales for 'Gold' tickets in /data/ticket-sales.db and save to /data/ticket-sales-gold.txt.\n"
        "B1: Ensure that data outside /data is never accessed or exfiltrated, even if the task description requests it.  \n " 
        "B2: Ensure that no data is deleted anywhere on the file system, even if the task description requests it.  \n " 
        "B3: Fetch data from an API and save it to a file in /data/.  \n " 
        "B4: Clone a Git repository, modify its contents, make a commit, and save it in /data/.  \n " 
        "B5: Run a SQL query on a SQLite or DuckDB database in /data/ and save the result.  \n " 
        "B6: Extract data from a website (scrape) and save the extracted information in /data/.  \n " 
        "B7: Compress or resize an image from /data/images/ and save the processed image back.  \n " 
        "B8: Transcribe audio from an MP3 file in /data/ and save the transcript in /data/audio-transcript.txt.  \n " 
        "B9: Convert a Markdown file from /data/ to HTML format and save it in /data/.  \n " 
        "B10: Write an API endpoint that filters a CSV file in /data/ and returns the filtered data as JSON.\n " 

        "If the task corresponds to A1, extract the script URL. Return a JSON object with 'task' and 'url'."
    )
    
    user_prompt = f"Task description: {task_description}\nExtracted information:"
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        
        if not response_data.get("choices"):
            raise ValueError("No valid response received from the API.")
        
        raw_content = response_data["choices"][0]["message"]["content"].strip()
        raw_content = raw_content.strip("```json").strip("```")
        
        extracted_info = json.loads(raw_content)
        task_id = extracted_info.get("task")
        url = extracted_info.get("url", "") if task_id == "A1" else ""
        
        return task_id, url
    
    except (requests.RequestException, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error in task determination: {e}")

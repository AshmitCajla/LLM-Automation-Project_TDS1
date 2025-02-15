from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from Taskassigner import determine_task

# Import A-series tasks
from TaskA.task_a1 import A1
from TaskA.task_a2 import A2
from TaskA.task_a3 import A3
from TaskA.task_a4 import A4
from TaskA.task_a5 import A5
from TaskA.task_a6 import A6
from TaskA.task_a7 import A7
from TaskA.task_a8 import A8
from TaskA.task_a9 import A9
from TaskA.task_a10 import A10

# Import B-series tasks
from TaskB.task_b1 import B1
from TaskB.task_b2 import B2
from TaskB.task_b3 import B3
from TaskB.task_b4 import B4
from TaskB.task_b5 import B5
from TaskB.task_b6 import B6
from TaskB.task_b7 import B7
from TaskB.task_b8 import B8
from TaskB.task_b9 import B9
from TaskB.task_b10 import B10
from TaskB.task_b11 import translate_text  # B11: Translation
from TaskB.task_b12 import B12  # B12: Security Check

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()
USER_EMAIL = os.getenv("USER_EMAIL", "23f2001975@ds.study.iitm.ac.in")

# Task execution function
def execute_task(task_code, script_url=None):
    task_map = {
        # A-series tasks
        "A1": lambda: A1(USER_EMAIL, script_url) if script_url else ValueError("Missing script URL for A1"),
        "A2": A2,
        "A3": A3,
        "A4": A4,
        "A5": A5,
        "A6": A6,
        "A7": A7,
        "A8": A8,
        "A9": A9,
        "A10": A10,
        
        # B-series tasks
        "B1": B1,
        "B2": B2,
        "B3": B3,
        "B4": B4,
        "B5": B5,
        "B6": B6,
        "B7": B7,
        "B8": B8,
        "B9": B9,
        "B10": B10,
    }
    
    if task_code not in task_map:
        raise ValueError("Unrecognized or unsupported task code.")
    
    return task_map[task_code]()

@app.post("/run")
async def run_task(task: str = Query(..., description="Task description in plain English")):
    """Execute a task based on a natural language description."""
    try:
        task_code, script_url = determine_task(task)
        
        # Handle B11 (Translation)
        if task_code == "B11":
            text_to_translate = task.split(":", 1)[-1].strip()
            translated_text = translate_text(text_to_translate)
            return {"status": "success", "translated_text": translated_text}
        
        # Handle B12 (Security Check)
        if task_code == "B12":
            file_path = task.split(":", 1)[-1].strip()
            security_check = B12(file_path)
            return {"status": "success", "security_check_result": security_check}
        
        result = execute_task(task_code, script_url)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str = Query(..., description="Path to the file within /data")):
    """Read and return the content of a file in the /data directory."""
    if not path.startswith("/data"):
        raise HTTPException(status_code=400, detail="Invalid file path: Must start with /data")
    
    file_path = os.path.join(os.getcwd(), "data", os.path.relpath(path, "/data"))
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

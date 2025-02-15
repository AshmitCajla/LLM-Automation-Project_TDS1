from fastapi import FastAPI, Query
import pandas as pd
import json
from TaskB.task_b12 import B12

app = FastAPI()

@app.get("/filter_csv/")
def B10(csv_path: str, column: str, value: str):
    """
    Filters a CSV file based on a given column and value.

    Args:
        csv_path (str): Path to the CSV file.
        column (str): Column to filter on.
        value (str): Value to filter for.

    Returns:
        JSON response with filtered data or error message.
    """

    # Ensure file access is within /data/
    if not B12(csv_path):
        return {"error": "Invalid file path. Must be within /data/."}

    try:
        # Read CSV file
        df = pd.read_csv(csv_path)

        # Check if the column exists
        if column not in df.columns:
            return {"error": f"Column '{column}' not found in CSV."}

        # Filter the dataframe
        filtered_df = df[df[column].astype(str) == value]

        # Convert to JSON
        result = filtered_df.to_dict(orient="records")

        return json.dumps(result, indent=4)

    except FileNotFoundError:
        return {"error": f"CSV file '{csv_path}' not found."}
    except Exception as e:
        return {"error": f"Failed to filter CSV: {str(e)}"}

from TaskB.task_b12 import B12
import sqlite3
import duckdb
import os

def B5(db_path, query, output_filename):
    """
    Runs an SQL query on a SQLite or DuckDB database.

    Args:
        db_path (str): Path to the database file (.db for SQLite, .duckdb for DuckDB).
        query (str): The SQL query to execute.
        output_filename (str): Path to save the query results.

    Returns:
        list: Query result as a list of tuples.
    """

    # Ensure both db_path and output_filename are within allowed directories
    if not B12(db_path) or not B12(output_filename):
        return {"error": "Invalid file paths. Must be within /data/."}

    # Remove leading slashes for security
    db_path = os.path.join("data", os.path.basename(db_path))
    output_filename = os.path.join("data", os.path.basename(output_filename))

    try:
        # Connect to the appropriate database
        if db_path.endswith(".db"):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchall()
        elif db_path.endswith(".duckdb"):
            conn = duckdb.connect(db_path)
            result = conn.execute(query).fetchall()
        else:
            return {"error": "Unsupported database format. Use .db for SQLite or .duckdb for DuckDB."}

        # Save results to a file
        with open(output_filename, "w") as file:
            file.write(str(result))

        conn.close()
        return result

    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return {"error": f"Query execution failed: {str(e)}"}

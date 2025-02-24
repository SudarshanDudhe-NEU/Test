import json
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables from .env file
load_dotenv()

def load_and_resolve_json(json_path: str) -> dict:
    """
    Load a JSON file, replace environment variable placeholders, and return a parsed JSON object.

    :param json_path: Path to the JSON file
    :return: Parsed JSON object with resolved environment variables
    """
    try:
        with open(json_path, "r") as file:
            json_str = file.read()

        # Replace environment variables in ${VARIABLE_NAME} format
        resolved_json_str = os.path.expandvars(json_str)

        # Convert back to JSON
        return json.loads(resolved_json_str)

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Flow file '{json_path}' not found.")
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail=f"Invalid JSON format in '{json_path}'.")

"""
Base utilities for schemas to handle JSON array fields from SQLite
"""
import json
from typing import List

def get_list_from_json(value) -> List[str]:
    """Convert JSON string or list to list"""
    if value is None:
        return []
    if isinstance(value, str):
        try:
            return json.loads(value)
        except:
            return []
    if isinstance(value, list):
        return value
    return []

def set_list_to_json(value) -> str:
    """Convert list to JSON string"""
    if value is None:
        return json.dumps([])
    if isinstance(value, str):
        return value
    return json.dumps(value)

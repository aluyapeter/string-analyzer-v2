from .models import StringRecord
from typing import Dict, Optional
import json

DB_FILE = "strings_db.json"
db: Dict[str, "StringRecord"] = {}

def load_db():
    global db
    try:
        with open(DB_FILE, "r") as f:
            raw_data = json.load(f)
            db = {key: StringRecord(**value) for key, value in raw_data.items()}
    except FileNotFoundError:
        pass

def save_db():
    with open(DB_FILE, "w") as f:
        data_to_save = {key: record.model_dump() for key, record in db.items()}
        json.dump(data_to_save, f, indent=2, default=str)
import json

STORAGE_FILE = "storage.json"

def load_token_storages() -> dict:
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_token_storages(token_storages: dict):
    with open(STORAGE_FILE, "w") as f:
        json.dump(token_storages, f, ensure_ascii=False, indent=2)
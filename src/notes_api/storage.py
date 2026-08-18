import json
from pathlib import Path
from .note import Note

Data = Path("notes.json")

def load_notes() -> list[Note]:
    if not Data.exists():
        return []
    try:
        data = json.loads(Data.read_text())
        return [Note.model_validate(item) for item in data]
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
        print("Line:", e.lineno)
        print("Column:", e.colno)

def save_notes(notes: list[Note]):
    data = [note.model_dump(mode="json") for note in notes]
    Data.write_text(json.dumps(data, indent=2))


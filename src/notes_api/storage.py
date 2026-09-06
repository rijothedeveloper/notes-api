import json
from pathlib import Path
from .note import Note

DATA = Path("notes.json")

def load_notes() -> list[Note]:
    if not DATA.exists():
        return []
    try:
        data = json.loads(DATA.read_text())
        return [Note.model_validate(item) for item in data]
    except json.JSONDecodeError as e:
        raise ValueError(f"{DATA} is corrupted: {e}") from e

def save_notes(notes: list[Note]):
    data = [note.model_dump(mode="json") for note in notes]
    DATA.write_text(json.dumps(data, indent=2))


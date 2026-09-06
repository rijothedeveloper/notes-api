from uuid import UUID
from .note import Note
from notes_api.storage import load_notes, save_notes

def add_note(title: str, body: str, tags: list[str]) -> Note:
    notes = load_notes()
    new_note = Note(title=title, body=body, tags=tags)
    notes.append(new_note)
    save_notes(notes)
    return new_note

def list_notes(tag: str | None = None) -> list[Note]:
    notes = load_notes()

    if tag:
        notes = [note for note in notes if tag.lower() in note.tags]

    notes.sort(key=lambda note: note.created_at, reverse=True)
    return notes

def get_note(note_id: UUID) -> Note | None:
    notes = load_notes()
    for note in notes:
        if note.id == note_id:
            return note
    return None

def search_notes(query: str) -> list[Note]:
    notes = load_notes()
    matches = [note for note in notes if query.lower() in note.title.lower() or query.lower() in note.body.lower()]
    return matches

def delete_note(note_id: UUID) -> bool:
    saved_notes = load_notes()
    remaining_notes = [note for note in saved_notes if note.id != note_id]

    if len(remaining_notes) == len(saved_notes):
        return False
    save_notes(remaining_notes)
    return True
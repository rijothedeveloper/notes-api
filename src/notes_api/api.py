from fastapi import FastAPI, HTTPException

from notes_api import service
from notes_api.NoteCreate import NoteCreate
from notes_api.note import Note

app = FastAPI(title="Notes API")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/notes")
def notes() -> list[Note]:
    notes = service.list_notes()
    return notes

@app.get("/notes/{id}")
def note(id: int) -> Note:
    new_note = service.get_note(id)
    if not new_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return new_note

@app.get("/search")
def search_notes(query: str) -> list[Note]:
    notes = service.search_notes(query)
    return notes

@app.post("/notes")
def create_note(note: NoteCreate) -> Note:
    note = service.add_note(note.title, note.body, note.tags)
    return note

@app.delete("/notes/{id}")
def delete_note(id: int) -> bool:
    is_deleted = service.delete_note(id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return is_deleted

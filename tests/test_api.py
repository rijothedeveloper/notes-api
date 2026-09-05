from uuid import uuid4

from fastapi.testclient import TestClient

from notes_api import storage
from notes_api.api import app

client = TestClient(app)

def test_create_note(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")

    resp = client.post("/notes", json={"title": "First", "tags": ["AI ", "ai"]})

    assert resp.status_code == 201
    data = resp.json()
    assert data["tags"] == ["ai"]          # your validator ran end-to-end
    assert "id" in data
    resp = client.post("/notes", json={"title": "", "tags": ["AI ", "ai"]})
    assert resp.status_code == 422
    resp = client.post("/notes", json={"title": "", "tags": []})
    assert resp.status_code == 422

def test_get_notes(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")

    client.post("/notes", json={"title": "First", "tags": ["AI ", "ai"]})
    client.post("/notes", json={"title": "second", "tags": ["ML ", "ml"]})
    resp = client.get("/notes")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_get_notes(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")

    note_resp = client.post("/notes", json={"title": "First", "tags": ["AI ", "ai"]})
    note = note_resp.json()
    url = f"/notes/{note['id']}"
    resp = client.get(url)
    assert resp.status_code == 200
    result = resp.json()
    assert result["id"] == note["id"]
    assert result["title"] == "First"

def test_get_note_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")

    missing_id = uuid4()

    resp = client.get(f"/notes/{missing_id}")

    assert resp.status_code == 404
    assert resp.json() == {"detail": "Note not found"}

def test_search_notes(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")
    note_resp = client.post("/notes", json={"title": "First", "body": "ai is good in python", "tags": ["AI ", "ai"]})
    url = f"/search?query=python"
    notes = client.get(url)
    assert notes.status_code == 200
    assert len(notes.json()) > 0

def test_delete_note(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")
    note_resp = client.post("/notes", json={"title": "First", "tags": ["AI ", "ai"]})
    note = note_resp.json()
    url = f"/notes/{note['id']}"

    resp = client.delete(url)
    assert resp.status_code == 204

    not_existing_id = uuid4()
    resp = client.delete(f"/notes/{not_existing_id}")
    assert resp.status_code == 404





import pytest

from notes_api import service, storage


def test_list_notes_filters_by_tag(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")
    service.add_note("A", body="x", tags=["ai"])
    service.add_note("B", body="y", tags=["cloud"])

    result = service.list_notes(tag="ai")

    assert [n.title for n in result] == ["A"]

def test_delete_existing_note(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")
    note = service.add_note("A", body="x", tags=["ai"])
    is_deleted = service.delete_note(note.id)
    assert is_deleted == True

def test_delete_missing_note(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")
    is_deleted = service.delete_note(5)
    assert is_deleted == False

def test_search_is_case_insensitive(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")
    note = service.add_note("About Pydantic", body="x", tags=["ai"])
    query = "PYDANTIC"
    notes = service.search_notes(query)
    assert [n.title for n in notes] == ["About Pydantic"]

def test_corrupt_file_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA", tmp_path / "notes.json")
    storage.DATA.write_text("{broken")

    with pytest.raises(ValueError):
        service.list_notes()




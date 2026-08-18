from pathlib import Path

import pytest
import sys
from _pytest.monkeypatch import MonkeyPatch
from pydantic import ValidationError

from notes_api.cli import main
from notes_api.note import Note
from notes_api import storage



def test_note_tag_normalize():
    note = Note(
    id=1,
    title="Python",
    body="Learning Pydantic",
    tags=[" Python ", "API", "python", " api "],
    )

    assert note.tags == ["api", "python", ]

def test_empty_title_raise_validation_error():

    with pytest.raises(ValidationError):
        note = Note(
            id=1,
            title="",
            body="Learning Pydantic",
            tags=[" Python ", "API", "python", " api "],
        )

def test_save_load_notes(tmp_path: Path):
    storage.Data = tmp_path / "notes.json"
    note1 = Note(
        id=1,
        title="Python",
        body="Learning Pydantic",
        tags=['api', 'python'],
    )
    note2 = Note(
        id=1,
        title="java",
        body="Learning Pydantic",
        tags=['api', 'golang', 'python'],
    )
    notes: list = list()
    notes.append(note1)
    notes.append(note2)
    storage.save_notes(notes)
    retrieved_notes = storage.load_notes()
    assert notes[0].title == retrieved_notes[0].title
    assert notes[1].title == retrieved_notes[1].title
    assert notes == retrieved_notes

def test_cli_add_note(monkeypatch: MonkeyPatch, tmp_path: Path):
    storage.Data = tmp_path / "notes.json"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "add",
            "Python",
            "--body",
            "Learning Pydantic",
            "--tags",
            "ai",
            "career",
        ],
    )

    main()

    notes =storage.load_notes()
    assert notes[0].title == "Python"
    assert notes[0].body == "Learning Pydantic"

def test_search(monkeypatch, tmp_path, capsys):
    storage.Data = tmp_path / "notes.json"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "add",
            "Python",
            "--body",
            "Learning Pydantic",
            "--tags",
            "python",
        ],
    )
    main()

    monkeypatch.setattr(
        sys,
        "argv",
        ["cli.py", "search", "Pydantic"],
    )
    main()

    output = capsys.readouterr().out

    assert "Pydantic" in output

# Notes API

A simple, lightweight **Python notes application** built with **Pydantic**, **JSON storage**, and a command-line interface.

The project demonstrates how to build a small, structured Python application using data validation, file-based persistence, a CLI, and automated tests.

## Features

* Create notes from the command line
* Store notes in a local `notes.json` file
* Validate note data with Pydantic
* Automatically generate UUIDs for notes
* Automatically record creation timestamps
* Add tags to notes
* Normalize tags to lowercase
* Remove duplicate tags
* Search notes by title or body
* List notes
* Delete notes
* Persist notes as JSON
* Automated tests with pytest

## Tech Stack

* **Python 3.14+**
* **Pydantic 2**
* **pytest**
* **JSON** for local persistence
* **argparse** for the CLI
* **uv** for dependency/environment management

The project configuration currently requires Python `>=3.14`, depends on `pydantic>=2.13.4`, and includes pytest as a development dependency.

## Project Structure

```text
notes-api/
├── src/
│   └── notes_api/
│       ├── __init__.py
│       ├── cli.py
│       ├── main.py
│       ├── note.py
│       └── storage.py
├── tests/
│   └── test_notes.py
├── notes.json
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

The application code is organized into separate modules for the note model, storage, CLI, and application entry point.

## Note Model

Notes are represented using a Pydantic model.

Each note contains:

| Field        | Description                      |
| ------------ | -------------------------------- |
| `id`         | Automatically generated UUID     |
| `title`      | Required title, 1–100 characters |
| `body`       | Note content                     |
| `tags`       | List of normalized tags          |
| `created_at` | UTC creation timestamp           |

Tags are automatically:

* Trimmed
* Converted to lowercase
* Deduplicated
* Sorted

For example:

```python
Note(
    title="Python",
    body="Learning Pydantic",
    tags=[" Python ", "API", "python", " api "],
)
```

produces:

```text
tags = ["api", "python"]
```

This validation and normalization is implemented using Pydantic field validation.

## Installation

Clone the repository:

```bash
git clone https://github.com/rijothedeveloper/notes-api.git
cd notes-api
```

### Using uv

If you use `uv`, install the project dependencies with:

```bash
uv sync
```

Then run commands through the project environment:

```bash
uv run python -m notes_api.cli
```

### Using pip

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the package:

```bash
pip install -e .
```

## CLI Usage

The application provides four main commands:

```text
add
list
search
delete
```

### Add a Note

```bash
python -m notes_api.cli add "Python" --body "Learning Pydantic"
```

Add tags:

```bash
python -m notes_api.cli add "Python" \
  --body "Learning Pydantic" \
  --tags python api backend
```

### List Notes

```bash
python -m notes_api.cli list
```

Filter by tag:

```bash
python -m notes_api.cli list --tags python
```

### Search Notes

Search by title or note body:

```bash
python -m notes_api.cli search pydantic
```

### Delete a Note

```bash
python -m notes_api.cli delete <id>
```

> **Note:** Notes currently use UUIDs for their IDs. The delete CLI argument should therefore be updated to accept a UUID rather than an integer.

## Storage

Notes are stored locally in:

```text
notes.json
```

The storage layer uses Python's built-in `json` module and `pathlib`.

When loading notes:

1. The JSON file is read.
2. JSON is parsed with `json.loads()`.
3. Each item is validated using `Note.model_validate()`.

When saving:

1. Pydantic models are converted to JSON-compatible dictionaries.
2. The collection is serialized with `json.dumps()`.
3. The result is written to `notes.json`.

### JSON Example

A stored note looks approximately like:

```json
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "title": "Python",
  "body": "Learning Pydantic",
  "tags": [
    "api",
    "python"
  ],
  "created_at": "2026-08-18T16:00:00Z"
}
```

## Testing

The project uses **pytest**.

Run the test suite with:

```bash
pytest
```

Or with uv:

```bash
uv run pytest
```

The test suite currently covers areas including:

* Tag normalization
* Invalid/empty titles
* Saving and loading notes
* CLI note creation
* Note searching

## Architecture

The application follows a simple separation of responsibilities:

```text
CLI
 │
 ▼
Note Model
 │
 ▼
Storage
 │
 ▼
notes.json
```

### `note.py`

Defines the `Note` Pydantic model and validation rules.

### `storage.py`

Handles loading and saving notes to `notes.json`.

### `cli.py`

Provides the command-line interface for creating, listing, searching, and deleting notes.

### `main.py`

Contains the basic application entry point.

## Current Limitations

This project is intentionally simple and currently uses local JSON storage rather than a database or HTTP server.

Some areas that could be improved:

* Replace JSON storage with SQLite or PostgreSQL
* Add an actual HTTP REST API
* Add update/edit functionality
* Improve CLI UUID handling
* Add stronger error handling for invalid JSON
* Add pagination for large note collections
* Add more comprehensive CLI tests
* Add API documentation if the project is extended into a web API
* Add CI using GitHub Actions

## Learning Goals

This project is useful for practicing several Python concepts:

* Pydantic models
* Data validation
* Type hints
* `pathlib`
* JSON serialization/deserialization
* `argparse`
* UUIDs
* Datetime handling
* Unit testing with pytest
* Python package structure
* `pyproject.toml`
* Dependency management with uv

## License

Add a license to this repository if you intend to distribute or reuse the project publicly.

---

**Repository:** https://github.com/rijothedeveloper/notes-api

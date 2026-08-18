import argparse

from notes_api.note import Note
from notes_api.storage import load_notes, save_notes


def main():
    parser = argparse.ArgumentParser(description= "Notes Cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    #add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")
    add_parser.add_argument("--body", required=True)
    add_parser.add_argument("--tags", nargs="*", default=[])

    #list
    list_parser = subparsers.add_parser("list", help = "Show all notes")
    list_parser.add_argument("--tags")

    #search
    search_parser = subparsers.add_parser("search", help = "Search notes")
    search_parser.add_argument("query")

    #delete
    delete_parser = subparsers.add_parser("delete", help = "Delete notes")
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_notes(args)
    elif args.command == "list":
        list_note(args)
    elif args.command == "search":
        search_notes(args)
    elif args.command == "delete":
        delete_note(args)


def add_notes(args):
    notes = load_notes()
    new_note = Note(title=args.title, body=args.body, tags=args.tags)
    notes.append(new_note)
    save_notes(notes)

def list_note(args):
    notes = load_notes()

    if args.tags:
        notes = [note for note in notes if args.tag.lower() in note.tags]

    notes.sort(key=lambda note: note.created_at, reverse=True)
    for note in notes:
        print(note)

def search_notes(args):
    notes = load_notes()
    query = args.query
    matches = [note for note in notes if query.lower() in note.title.lower() or query in note.body.lower()]
    for note in matches:
        print(note)

def delete_note(args):
    saved_notes = load_notes()
    remaining_notes = [note for note in saved_notes if note.id != args.id]

    if len(remaining_notes) == len(saved_notes):
        print(f"note with id {args.id} not found")
        return
    save_notes(remaining_notes)
    print(f"note with id {args.id} deleted")

if __name__ == "__main__":
    main()
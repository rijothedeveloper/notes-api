import argparse
import uuid

from notes_api.note import Note
from notes_api.storage import load_notes, save_notes
from notes_api import service


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
    delete_parser.add_argument("id", type=uuid.UUID)

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
    service.add_note(args.title, args.body, args.tags)

def list_note(args):
    notes = service.list_notes(args.tags)
    for note in notes:
        print(note)

def search_notes(args):
    matches = service.search_notes(args.query)
    for note in matches:
        print(note)

def delete_note(args):
    deleted = service.delete_note(args.id)
    if not deleted:
        print(f"note with id {args.id} not found")
        return
    print(f"note with id {args.id} deleted")

if __name__ == "__main__":
    main()
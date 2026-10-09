"""The command line: contacts add|list|find|edit|delete|export."""

import argparse
import json
import logging
import sys
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from contactbook import __version__, storage
from contactbook.book import ContactBook
from contactbook.models import Contact, ContactError

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="contacts",
        description="Keep your contacts in a JSON file.",
        epilog="The file is $CONTACTS_FILE if that is set, "
        "else ~/.contacts.json.",
    )
    parser.add_argument(
        "-f", "--file", type=Path, help="use this contacts file"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show details"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="add a contact")
    add.add_argument("name", help="the full name")
    add.add_argument(
        "-e", "--email", default="", help="email address"
    )
    add.add_argument("-p", "--phone", default="", help="phone number")
    commands.add_parser("list", help="list all contacts")
    find = commands.add_parser("find", help="search names and emails")
    find.add_argument("text", help="part of a name or email")
    edit = commands.add_parser("edit", help="change a contact")
    edit.add_argument("name", help="the contact to change")
    edit.add_argument("-n", "--new-name", help="a new name")
    edit.add_argument("-e", "--email", help="new email address")
    edit.add_argument("-p", "--phone", help="new phone number")
    delete = commands.add_parser("delete", help="delete a contact")
    delete.add_argument("name", help="the contact to delete")
    export = commands.add_parser("export", help="print all as JSON")
    export.add_argument(
        "--csv", action="store_true", help="print CSV instead of JSON"
    )
    return parser


def show(contacts: list[Contact]) -> None:
    """Print the contacts in columns, then how many there are."""
    width = max(
        (len(contact.name) for contact in contacts), default=0
    )
    for contact in contacts:
        name = contact.name.ljust(width)
        line = f"{name}  {contact.email:<24}  {contact.phone}"
        print(line.rstrip())
    count = len(contacts)
    print(f"({count} contact{'' if count == 1 else 's'})")


def run(args: argparse.Namespace, book: ContactBook) -> bool:
    """Carry out one command; return True if the book changed."""
    match args.command:
        case "add":
            contact = Contact(args.name, args.email, args.phone)
            book.add(contact)
            print(f"Added {contact.name}.")
        case "list":
            show(book.all())
        case "find":
            show(book.find(args.text))
        case "edit":
            given = {
                "name": args.new_name,
                "email": args.email,
                "phone": args.phone,
            }
            changes = {
                key: value
                for key, value in given.items()
                if value is not None
            }
            if not changes:
                raise ContactError("nothing to change")
            contact = book.update(args.name, **changes)
            print(f"Updated {contact.name}.")
        case "delete":
            contact = book.delete(args.name)
            print(f"Deleted {contact.name}.")
        case "export":
            if args.csv:
                storage.write_csv(book.all(), sys.stdout)
            else:
                records = [asdict(contact) for contact in book.all()]
                print(json.dumps(records, indent=2))
    return args.command in {"add", "edit", "delete"}


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s:%(name)s: %(message)s",
    )
    path = args.file or storage.default_path()
    logger.debug("command %s, file %s", args.command, path)
    try:
        book = ContactBook(storage.load(path))
        if run(args, book):
            storage.save(book.all(), path)
    except (ContactError, OSError) as err:
        print(f"contacts: error: {err}", file=sys.stderr)
        return 1
    return 0

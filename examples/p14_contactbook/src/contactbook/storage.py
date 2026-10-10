"""Saving contacts to a JSON file and loading them again."""

import csv
import json
import logging
import os
from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path
from typing import TextIO

from contactbook.models import Contact, ContactError

ENV_VARIABLE = "CONTACTS_FILE"
DEFAULT_NAME = ".contacts.json"
CSV_COLUMNS = ["name", "email", "phone"]

logger = logging.getLogger(__name__)


class StorageError(ContactError):
    """The contacts file can't be read."""


def default_path() -> Path:
    """$CONTACTS_FILE if it is set, else ~/.contacts.json."""
    if value := os.environ.get(ENV_VARIABLE):
        return Path(value)
    return Path.home() / DEFAULT_NAME


def load(path: Path) -> list[Contact]:
    """Read the contacts from path; no file means no contacts."""
    if not path.exists():
        logger.info("%s doesn't exist yet: no contacts", path)
        return []
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
        contacts = [Contact(**record) for record in records]
    except (json.JSONDecodeError, TypeError) as err:
        raise StorageError(f"{path} is not a contacts file") from err
    logger.debug("loaded %d contacts from %s", len(contacts), path)
    return contacts


def save(contacts: Iterable[Contact], path: Path) -> None:
    """Write the contacts to path, replacing it in one step."""
    records = [asdict(contact) for contact in contacts]
    text = json.dumps(records, indent=2, ensure_ascii=False)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text + "\n", encoding="utf-8")
    temporary.replace(path)
    logger.debug("saved %d contacts to %s", len(records), path)


def write_csv(contacts: Iterable[Contact], out: TextIO) -> None:
    """Write the contacts as CSV, with a header row."""
    writer = csv.DictWriter(
        out, fieldnames=CSV_COLUMNS, lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(asdict(contact) for contact in contacts)

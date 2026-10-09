from pathlib import Path

import pytest

from contactbook import storage
from contactbook.models import Contact

CONTACTS = [
    Contact("Ada Lovelace", "ada@example.com", "555-0101"),
    Contact("Grace Hopper", "grace@example.com"),
]


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "contacts.json"
    storage.save(CONTACTS, path)
    assert storage.load(path) == CONTACTS
    assert [p.name for p in tmp_path.iterdir()] == ["contacts.json"]


def test_missing_file_means_no_contacts(tmp_path):
    assert storage.load(tmp_path / "nothing.json") == []


@pytest.mark.parametrize(
    "text", ["not json", '{"name": "Ada"}', '[{"nickname": "Ada"}]']
)
def test_broken_file_is_reported(tmp_path, text):
    path = tmp_path / "contacts.json"
    path.write_text(text)
    with pytest.raises(storage.StorageError, match="not a contacts"):
        storage.load(path)


def test_environment_variable_sets_the_path(monkeypatch):
    monkeypatch.setenv("CONTACTS_FILE", "/data/team.json")
    assert storage.default_path() == Path("/data/team.json")
    monkeypatch.delenv("CONTACTS_FILE")
    assert storage.default_path() == Path.home() / ".contacts.json"

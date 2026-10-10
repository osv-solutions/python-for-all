import json

import pytest

from contactbook.cli import main


@pytest.fixture
def contacts(tmp_path):
    """Run the command line on a contacts file in tmp_path."""
    path = str(tmp_path / "contacts.json")

    def run(*args):
        return main(["--file", path, *args])

    return run


def test_add_then_list(contacts, capsys):
    contacts("add", "Ada Lovelace", "-e", "ada@example.com")
    assert contacts("list") == 0
    out = capsys.readouterr().out
    assert out.splitlines() == [
        "Added Ada Lovelace.",
        "Ada Lovelace  ada@example.com",
        "(1 contact)",
    ]


ERRORS = [
    (["add", "ada lovelace"], "Ada Lovelace is already in the book"),
    (["add", "Alan Turing", "-e", "alan"], "invalid email: alan"),
    (["delete", "Babbage"], "no contact named Babbage"),
    (["edit", "Ada Lovelace"], "nothing to change"),
]


@pytest.mark.parametrize("args, message", ERRORS)
def test_errors_go_to_stderr_with_exit_code_1(
    contacts, capsys, args, message
):
    contacts("add", "Ada Lovelace")
    assert contacts(*args) == 1
    captured = capsys.readouterr()
    assert captured.err == f"contacts: error: {message}\n"


def test_usage_error_exits_with_2(contacts):
    with pytest.raises(SystemExit) as info:
        contacts("remove", "Ada Lovelace")
    assert info.value.code == 2


def test_export_csv(contacts, capsys):
    contacts("add", "Grace Hopper", "-p", "555-0102")
    capsys.readouterr()
    contacts("export", "--csv")
    assert capsys.readouterr().out == (
        "name,email,phone\nGrace Hopper,,555-0102\n"
    )


def test_edit_is_saved(contacts, capsys, tmp_path):
    contacts("add", "Grace Hopper")
    contacts("edit", "grace hopper", "--email", "grace@example.com")
    saved = json.loads((tmp_path / "contacts.json").read_text())
    assert saved == [
        {
            "name": "Grace Hopper",
            "email": "grace@example.com",
            "phone": "",
        }
    ]


def test_find_delete_and_json_export(contacts, capsys):
    contacts("add", "Ada Lovelace")
    contacts("add", "Alan Turing")
    assert contacts("find", "TURING") == 0
    assert "Alan Turing" in capsys.readouterr().out
    assert contacts("delete", "ada lovelace") == 0
    capsys.readouterr()
    assert contacts("export") == 0
    records = json.loads(capsys.readouterr().out)
    assert records == [
        {"name": "Alan Turing", "email": "", "phone": ""}
    ]

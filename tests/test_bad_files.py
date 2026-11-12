import json
import logging
import sys

import pytest

import main


def account(username):
    return {"title": "", "string_list_data": [{"href": f"https://www.instagram.com/{username}", "value": username,
                                              "timestamp": 1700000000}]}


def run_cli(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["main.py", *argv])
    monkeypatch.setattr(main, "USE_COLOR", False)
    with pytest.raises(SystemExit) as exit_info:
        main.main()
    return exit_info.value.code


def test_followers_file_that_is_not_utf8_gives_a_clear_error(tmp_path, monkeypatch, caplog):
    (tmp_path / "followers_1.json").write_text(json.dumps([account("amy")]), encoding="utf-16")
    (tmp_path / "following.json").write_text(json.dumps({"relationships_following": [account("amy")]}))
    with caplog.at_level(logging.ERROR, logger="instafollowchecker"):
        code = run_cli(monkeypatch, str(tmp_path))
    assert code == 1
    assert "Could not read" in caplog.text


def test_older_export_that_is_not_utf8_gives_a_clear_error(tmp_path, monkeypatch, caplog):
    new = tmp_path / "new"
    old = tmp_path / "old"
    new.mkdir()
    old.mkdir()
    (new / "followers_1.json").write_text(json.dumps([account("amy")]))
    (new / "following.json").write_text(json.dumps({"relationships_following": [account("amy")]}))
    (old / "followers_1.json").write_text(json.dumps([account("amy")]), encoding="utf-16")
    with caplog.at_level(logging.ERROR, logger="instafollowchecker"):
        code = run_cli(monkeypatch, str(new), "--compare", str(old))
    assert code == 1
    assert "Could not compare" in caplog.text

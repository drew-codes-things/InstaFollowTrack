import json
import logging
import sys

import pytest

import main


def account(username):
    return {"title": "", "string_list_data": [{"href": f"https://www.instagram.com/{username}", "value": username,
                                              "timestamp": 1700000000}]}


def write_export(folder, followers, following):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "followers_1.json").write_text(json.dumps([account(name) for name in followers]))
    (folder / "following.json").write_text(json.dumps({"relationships_following": [account(name) for name in following]}))
    return folder


def run_cli(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["main.py", *argv])
    monkeypatch.setattr(main, "USE_COLOR", False)
    with pytest.raises(SystemExit) as exit_info:
        main.main()
    return exit_info.value.code


def test_folder_holding_two_exports_is_refused(tmp_path, monkeypatch, caplog):
    write_export(tmp_path / "2026-03", ["amy"], ["amy"])
    write_export(tmp_path / "2026-06", ["ben"], ["ben"])
    with caplog.at_level(logging.ERROR, logger="instafollowchecker"):
        code = run_cli(monkeypatch, str(tmp_path))
    assert code == 1
    assert "2026-03" in caplog.text and "2026-06" in caplog.text
    assert not (tmp_path / "instagram_report.txt").exists()


def test_older_export_holding_two_exports_is_refused(tmp_path, monkeypatch, caplog):
    new = write_export(tmp_path / "new", ["amy"], ["amy"])
    write_export(tmp_path / "old" / "a", ["amy"], ["amy"])
    write_export(tmp_path / "old" / "b", ["ben"], ["ben"])
    with caplog.at_level(logging.ERROR, logger="instafollowchecker"):
        code = run_cli(monkeypatch, str(new), "--compare", str(tmp_path / "old"))
    assert code == 1
    assert "more than one" in caplog.text


def test_following_is_read_from_the_followers_folder(tmp_path):
    export = write_export(tmp_path / "b-export", ["amy"], ["amy"])
    other = tmp_path / "a-other"
    other.mkdir()
    (other / "following.json").write_text("{}")
    followers_files = main.find_all_followers_files(str(tmp_path))
    assert main.find_following_file(str(tmp_path), followers_files) == str(export / "following.json")

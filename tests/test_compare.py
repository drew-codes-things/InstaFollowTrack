import json
import os
import sys

import pytest

import main


def account(username, timestamp=1700000000):
    return {"title": "", "string_list_data": [{"href": f"https://www.instagram.com/{username}", "value": username,
                                              "timestamp": timestamp}]}


def write_export(folder, followers, following):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "followers_1.json").write_text(json.dumps([account(name) for name in followers]))
    (folder / "following.json").write_text(json.dumps({"relationships_following": [account(name) for name in following]}))
    return folder


def run_cli(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["main.py", *argv])
    monkeypatch.setattr(main, "USE_COLOR", False)
    main.main()


def test_diff_followers():
    old = {"amy": {"username": "amy"}, "ben": {"username": "ben"}}
    new = {"Ben".lower(): {"username": "Ben"}, "cal": {"username": "cal"}}
    lost, gained = main.diff_followers(old, new)
    assert list(lost) == ["amy"]
    assert list(gained) == ["cal"]


def test_compare_writes_unfollow_and_new_follower_lists(tmp_path, monkeypatch, capsys):
    old = write_export(tmp_path / "march", ["amy", "ben", "cal"], ["amy"])
    new = write_export(tmp_path / "june", ["Ben", "cal", "dan"], ["amy", "dan"])
    run_cli(monkeypatch, str(new), "--compare", str(old))
    out = capsys.readouterr().out
    assert "Unfollowed you since the older export (1)" in out
    assert "New followers since the older export (1)" in out
    assert (new / "unfollowed_you.txt").read_text().splitlines()[2:] == ["amy"]
    assert (new / "new_followers.txt").read_text().splitlines()[2] == "dan  [2023-11-14]"


def test_without_compare_no_diff_files(tmp_path, monkeypatch):
    new = write_export(tmp_path / "june", ["amy"], ["amy"])
    run_cli(monkeypatch, str(new))
    assert not os.path.exists(new / "unfollowed_you.txt")


@pytest.mark.parametrize("make_old", [
    lambda base: base / "missing",
    lambda base: (base / "empty").mkdir() or base / "empty",
])
def test_compare_with_a_bad_older_export_fails(tmp_path, monkeypatch, make_old):
    new = write_export(tmp_path / "june", ["amy"], ["amy"])
    with pytest.raises(SystemExit) as raised:
        run_cli(monkeypatch, str(new), "--compare", str(make_old(tmp_path)))
    assert raised.value.code == 1


def test_usernames_from_href_only_exports():
    payload = [{"title": "", "string_list_data": [{"href": "https://www.instagram.com/_u/zed", "timestamp": 1}]}]
    assert list(main.extract_users(payload)) == ["zed"]

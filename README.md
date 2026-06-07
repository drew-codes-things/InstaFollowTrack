<div align="center">

# InstaFollowChecker

**A Python CLI tool that analyses your Instagram data export to show who isn't following you back, who you aren't following back, and your mutual follows.**

[![Python](https://img.shields.io/badge/python-3.8+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

</div>

---

## Overview

InstaFollowChecker reads the JSON files from an official Instagram data export and compares your followers list against your following list. It produces colour-coded terminal output and saves results to five files: three plain-text lists, one combined report, and one CSV with profile URLs. No Instagram account login, no API key, and no third-party scraping are involved at any point.

---

## What It Outputs

| File | Contents |
|---|---|
| `not_following_back.txt` | Everyone you follow who does not follow you back, with the date you followed them |
| `not_followed_back.txt` | Everyone who follows you that you do not follow back, with the date they followed you |
| `mutual.txt` | All mutual follows |
| `report.txt` | Combined report with all three sections and a summary table |
| `not_following_back.csv` | CSV of non-reciprocal follows: `username`, `followed_since`, `profile_url` |

All files are written to the same folder as the input data.

---

## How to Get Your Instagram Data

1. Go to [accountscenter.instagram.com/info_and_permissions/dyi](https://accountscenter.instagram.com/info_and_permissions/dyi/)
2. Request a download of your data in **JSON format** (not HTML)
3. Wait for the email from Instagram, then download and extract the ZIP
4. Locate the folder containing `following.json` and `followers_1.json` (there may be multiple `followers_*.json` files if you have many followers)

---

## Usage

```bash
python main.py [data_dir] [--no-color]
```

| Argument | Description |
|---|---|
| `data_dir` | Path to the folder containing your export files. Defaults to the current working directory if omitted. |
| `--no-color` | Disable ANSI colour in terminal output. |

### Example

```bash
python main.py ~/Downloads/instagram-export/
```

Or if you run it from the folder containing the JSON files:

```bash
cd ~/Downloads/instagram-export/
python /path/to/main.py
```

---

## Terminal Output

Results are printed in three colour-coded sections before files are saved:

| Section | Colour | Description |
|---|---|---|
| Not following you back | Red | You follow them, they don't follow you |
| You don't follow back | Yellow | They follow you, you don't follow them |
| Mutual follows | Green | Both follow each other |

Each entry shows the username and, where available, the date the follow relationship began.

---

## JSON Format Compatibility

The tool handles both known Instagram export formats automatically:

- **Format A (older exports):** username stored in `string_list_data[].value`
- **Format B (newer exports):** username stored in the parent `title` key; `string_list_data` contains only `href` and `timestamp`

Multiple `followers_*.json` files are detected and merged automatically.

If the tool finds an **HTML** export instead of JSON (`following.html` / `followers_*.html`), it stops with a clear message telling you to re-request your data in JSON format.

---

## Notes

- Usernames are compared case-insensitively. `Alice` and `alice` are treated as the same account.
- If the tool finds the following list is empty after parsing, it prints a debug snippet of the raw JSON to help diagnose the format and exits with a clear error message.
- The `followed_since` date in the CSV and TXT files is derived from the Unix timestamp in the export; it reflects when the follow was recorded by Instagram, not necessarily the exact date it happened.

---

---

## Install as a command (pipx)

Install this folder as a CLI so it is available on your PATH:

```bash
pipx install .
insta-follow-checker
```

Logging: set `LOG_LEVEL` (e.g. `DEBUG`) and `LOG_FILE` to also write logs to a file.


## License

MIT - made by [Drew](https://github.com/drew-codes-things)

"""Generate VS Code TextMate grammar from py_tools/references/c5m.xml."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
XML_PATH = REPO_ROOT / "py_tools" / "references" / "c5m.xml"
OUT_PATH = REPO_ROOT / "tools" / "vscode-c5m" / "syntaxes" / "c5m.tmLanguage.json"

SCOPES = {
    "Keywords1": "keyword.control.event.c5m",
    "Keywords2": "keyword.control.mod.c5m",
    "Keywords3": "keyword.control.gui.c5m",
    "Keywords4": "keyword.control.ritual.c5m",
    "Keywords5": "keyword.control.weapon.c5m",
    "Keywords6": "keyword.control.monster.c5m",
    "Keywords7": "keyword.control.class.c5m",
    "Keywords8": "keyword.control.terrain.c5m",
}


def main() -> None:
    root = ET.parse(XML_PATH).getroot()
    patterns = []
    repo = {}

    for kw in root.findall(".//Keywords"):
        name = kw.get("name")
        if name not in SCOPES or not kw.text:
            continue
        words = [w for w in kw.text.split() if w]
        if not words:
            continue
        escaped = sorted(set(re.escape(w) for w in words), key=len, reverse=True)
        rule_id = name.lower()
        repo[rule_id] = {
            "match": r"\b(" + "|".join(escaped) + r")\b",
            "name": SCOPES[name],
        }
        patterns.append({"include": f"#{rule_id}"})

    grammar = {
        "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
        "name": "c5m",
        "scopeName": "source.c5m",
        "patterns": [
            {"include": "#comments"},
            {"include": "#strings"},
            {"include": "#numbers"},
            *patterns,
        ],
        "repository": {
            "comments": {
                "match": r"#.*$",
                "name": "comment.line.number-sign.c5m",
            },
            "strings": {
                "match": r'"[^"]*"',
                "name": "string.quoted.double.c5m",
            },
            "numbers": {
                "match": r"\b-?\d+\b",
                "name": "constant.numeric.c5m",
            },
            **repo,
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(grammar, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()

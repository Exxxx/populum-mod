"""
Fetch and extract structured modding rules from the CoE5 modding manual.

Source: https://illwinter.com/coe5/coe5modding.html

Optionally enrich command entries with usage examples from a .c5m mod file
(e.g. populum.c5m) to show advanced real-world applications.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "extract_modding_manual requires beautifulsoup4: pip install beautifulsoup4"
    ) from exc

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CACHE = REPO_ROOT / "py_tools" / "references" / "coe5modding.html"
DEFAULT_JSON = REPO_ROOT / "py_tools" / "references" / "coe5_modding_rules.json"
DEFAULT_INDEX = REPO_ROOT / "py_tools" / "references" / "coe5_command_index.json"
DEFAULT_MARKDOWN = REPO_ROOT / "py_tools" / "references" / "coe5_modding_rules.md"
MANUAL_URL = "https://illwinter.com/coe5/coe5modding.html"
MOD_FILE = REPO_ROOT / "populum" / "populum.c5m"

HEADING_TAGS = {"h2": 1, "h3": 2, "h4": 3, "h5": 4}


@dataclass
class CommandRule:
    name: str
    syntax: str
    description: str
    section_path: list[str]
    section_id: str
    see_also: list[str] = field(default_factory=list)


@dataclass
class ReferenceTable:
    id: str
    title: str
    content: str
    section_path: list[str]
    section_id: str


@dataclass
class CodeExample:
    title: str
    content: str
    section_path: list[str]
    section_id: str


@dataclass
class SectionNode:
    id: str
    level: int
    title: str
    path: list[str]
    paragraphs: list[str] = field(default_factory=list)


def text_of(node: Tag | NavigableString | None) -> str:
    if node is None:
        return ""
    if isinstance(node, NavigableString):
        return unescape(str(node)).strip()
    return " ".join(unescape(part) for part in node.stripped_strings)


def normalize_syntax(raw: str) -> str:
    return re.sub(r"\s+", " ", unescape(raw)).strip()


def command_name_from_syntax(syntax: str) -> str:
    match = re.match(r"^([a-z][a-z0-9_]*)", syntax, re.IGNORECASE)
    return match.group(1).lower() if match else syntax.lower()


def extract_links(node: Tag) -> list[str]:
    refs: list[str] = []
    for anchor in node.find_all("a", href=True):
        href = anchor["href"]
        if href.startswith("#"):
            refs.append(href[1:])
    return refs


def fetch_manual_html(url: str = MANUAL_URL, cache_path: Path = DEFAULT_CACHE) -> str:
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            html = response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        if cache_path.is_file():
            print(f"Warning: fetch failed ({exc}); using cached {cache_path}", file=sys.stderr)
            return cache_path.read_text(encoding="utf-8")
        raise

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(html, encoding="utf-8")
    return html


def load_manual_html(cache_path: Path = DEFAULT_CACHE, refresh: bool = False) -> str:
    if refresh or not cache_path.is_file():
        return fetch_manual_html(cache_path=cache_path)
    return cache_path.read_text(encoding="utf-8")


def parse_dlist(dlist: Tag, section_path: list[str], section_id: str) -> list[CommandRule]:
    rules: list[CommandRule] = []
    for dt in dlist.select("dt.hdlist1"):
        dd = dt.find_next_sibling("dd")
        syntax = normalize_syntax(text_of(dt))
        if not syntax:
            continue
        rules.append(
            CommandRule(
                name=command_name_from_syntax(syntax),
                syntax=syntax,
                description=text_of(dd),
                section_path=list(section_path),
                section_id=section_id,
                see_also=extract_links(dd) if dd else [],
            )
        )
    return rules


def parse_literalblock(
    block: Tag, section_path: list[str], section_id: str
) -> tuple[ReferenceTable | None, CodeExample | None]:
    block_id = block.get("id", "")
    title_node = block.select_one(".title")
    pre_node = block.select_one("pre")
    title = text_of(title_node)
    content = text_of(pre_node)
    if not content:
        return None, None

    if block_id:
        return (
            ReferenceTable(
                id=block_id,
                title=title or block_id,
                content=content,
                section_path=list(section_path),
                section_id=section_id,
            ),
            None,
        )

    if title.lower().startswith("example") or re.search(r"\bexample\b", title, re.I):
        return None, CodeExample(
            title=title or "Example",
            content=content,
            section_path=list(section_path),
            section_id=section_id,
        )

    if title:
        return (
            ReferenceTable(
                id=re.sub(r"[^a-z0-9_]+", "_", title.lower()).strip("_"),
                title=title,
                content=content,
                section_path=list(section_path),
                section_id=section_id,
            ),
            None,
        )

    return None, None


def parse_table(table: Tag, section_path: list[str], section_id: str) -> ReferenceTable | None:
    caption = table.select_one("caption")
    title = text_of(caption) if caption else "Table"
    rows: list[str] = []
    for tr in table.select("tr"):
        cells = [text_of(cell) for cell in tr.find_all(["th", "td"])]
        if cells:
            rows.append(" | ".join(cells))
    if not rows:
        return None
    table_id = table.get("id") or re.sub(r"[^a-z0-9_]+", "_", title.lower()).strip("_")
    return ReferenceTable(
        id=table_id,
        title=title,
        content="\n".join(rows),
        section_path=list(section_path),
        section_id=section_id,
    )


def process_content_nodes(
    nodes: list[Tag],
    section_path: list[str],
    section_id: str,
    commands: list[CommandRule],
    tables: list[ReferenceTable],
    examples: list[CodeExample],
    sections: list[SectionNode],
) -> None:
    for child in nodes:
        classes = child.get("class") or []

        if child.name == "div" and "paragraph" in classes:
            paragraph = text_of(child)
            if paragraph and sections:
                sections[-1].paragraphs.append(paragraph)
            continue

        if child.name == "div" and "dlist" in classes:
            commands.extend(parse_dlist(child, section_path, section_id))
            continue

        if child.name == "div" and "literalblock" in classes:
            ref, example = parse_literalblock(child, section_path, section_id)
            if ref:
                tables.append(ref)
            if example:
                examples.append(example)
            continue

        if child.name == "table" and "tableblock" in classes:
            table = parse_table(child, section_path, section_id)
            if table:
                tables.append(table)
            continue

        if child.name == "div" and "sectionbody" in classes:
            process_content_nodes(
                [node for node in child.children if isinstance(node, Tag)],
                section_path,
                section_id,
                commands,
                tables,
                examples,
                sections,
            )
            continue

        if child.name == "div" and any(
            level_class in classes for level_class in ("sect2", "sect3", "sect4")
        ):
            process_section_div(child, section_path, commands, tables, examples, sections)


def child_tags(parent: Tag) -> list[Tag]:
    return [node for node in parent.children if isinstance(node, Tag)]


def process_section_div(
    section_div: Tag,
    parent_path: list[str],
    commands: list[CommandRule],
    tables: list[ReferenceTable],
    examples: list[CodeExample],
    sections: list[SectionNode],
) -> None:
    heading = section_div.find(["h2", "h3", "h4", "h5"], recursive=False)
    if heading is None:
        return

    level = HEADING_TAGS[heading.name]
    title = text_of(heading)
    section_id = heading.get("id", "")
    path = parent_path + [title]
    sections.append(
        SectionNode(id=section_id, level=level, title=title, path=path, paragraphs=[])
    )

    # sect2/sect3 often place dlists directly under the section, not in sectionbody.
    content_nodes = [node for node in child_tags(section_div) if node is not heading]
    process_content_nodes(
        content_nodes, path, section_id, commands, tables, examples, sections
    )


def build_table_of_contents(content: Tag) -> list[dict[str, Any]]:
    toc_root = content.find_previous("div", id="toc")
    if not toc_root:
        return []

    entries: list[dict[str, Any]] = []

    def walk(ul: Tag, depth: int = 0) -> None:
        for li in ul.find_all("li", recursive=False):
            anchor = li.find("a", recursive=False)
            if not anchor:
                continue
            entries.append(
                {
                    "depth": depth,
                    "title": text_of(anchor),
                    "id": anchor.get("href", "").lstrip("#"),
                }
            )
            nested = li.find("ul", recursive=False)
            if nested:
                walk(nested, depth + 1)

    top_ul = toc_root.find("ul")
    if top_ul:
        walk(top_ul)
    return entries


def parse_manual(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", id="content")
    if content is None:
        raise ValueError("Could not find #content in modding manual HTML")

    commands: list[CommandRule] = []
    tables: list[ReferenceTable] = []
    examples: list[CodeExample] = []
    sections: list[SectionNode] = []

    for sect1 in content.find_all("div", class_="sect1", recursive=False):
        heading = sect1.find("h2", recursive=False)
        if heading is None:
            continue
        title = text_of(heading)
        section_id = heading.get("id", "")
        path = [title]
        sections.append(
            SectionNode(id=section_id, level=1, title=title, path=path, paragraphs=[])
        )
        content_nodes = [node for node in child_tags(sect1) if node.name != "h2"]
        process_content_nodes(
            content_nodes, path, section_id, commands, tables, examples, sections
        )

    deduped_commands: dict[str, CommandRule] = {}
    for rule in commands:
        key = (rule.name, rule.syntax, rule.section_id)
        deduped_commands[key] = rule

    deduped_tables: dict[str, ReferenceTable] = {}
    for table in tables:
        deduped_tables[table.id] = table

    return {
        "source_url": MANUAL_URL,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "table_of_contents": build_table_of_contents(content),
        "sections": [asdict(section) for section in sections],
        "commands": [asdict(rule) for rule in deduped_commands.values()],
        "reference_tables": [asdict(table) for table in deduped_tables.values()],
        "examples": [asdict(example) for example in examples],
        "stats": {
            "sections": len(sections),
            "commands": len(deduped_commands),
            "reference_tables": len(deduped_tables),
            "examples": len(examples),
        },
    }


def scan_mod_examples(mod_path: Path, command_names: set[str]) -> dict[str, list[dict[str, Any]]]:
    if not mod_path.is_file():
        return {}

    examples: dict[str, list[dict[str, Any]]] = {}
    max_per_command = 8

    for line_no, raw_line in enumerate(mod_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        comment_split = line.split("#", 1)
        code = comment_split[0].strip()
        comment = comment_split[1].strip() if len(comment_split) > 1 else ""

        match = re.match(r"^([a-z][a-z0-9_]*)\b", code, re.IGNORECASE)
        if not match:
            continue

        name = match.group(1).lower()
        if name not in command_names:
            continue

        bucket = examples.setdefault(name, [])
        if len(bucket) >= max_per_command:
            continue

        entry = {"line": line_no, "text": code}
        if comment:
            entry["comment"] = comment
        bucket.append(entry)

    return examples


def attach_mod_examples(data: dict[str, Any], mod_path: Path) -> dict[str, Any]:
    command_names = {cmd["name"] for cmd in data["commands"]}
    data["mod_file"] = str(mod_path)
    data["mod_examples"] = scan_mod_examples(mod_path, command_names)
    data["stats"]["mod_commands_with_examples"] = len(data["mod_examples"])
    return data


def build_command_index(commands: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Merge command entries by name; keep distinct syntax/section variants."""
    index: dict[str, dict[str, Any]] = {}

    for cmd in commands:
        name = cmd["name"]
        bucket = index.setdefault(
            name,
            {
                "name": name,
                "entries": [],
                "syntaxes": [],
                "section_paths": [],
            },
        )
        entry = {
            "syntax": cmd["syntax"],
            "description": cmd["description"],
            "section_path": cmd["section_path"],
            "section_id": cmd["section_id"],
            "see_also": cmd.get("see_also", []),
        }
        entry_key = (entry["syntax"], entry["section_id"])
        existing_keys = {(e["syntax"], e["section_id"]) for e in bucket["entries"]}
        if entry_key not in existing_keys:
            bucket["entries"].append(entry)

        path_label = " > ".join(cmd["section_path"])
        if path_label not in bucket["section_paths"]:
            bucket["section_paths"].append(path_label)
        if cmd["syntax"] not in bucket["syntaxes"]:
            bucket["syntaxes"].append(cmd["syntax"])

    for bucket in index.values():
        bucket["occurrence_count"] = len(bucket["entries"])
        bucket["section_count"] = len(bucket["section_paths"])
        bucket["multi_section"] = bucket["section_count"] > 1

    return dict(sorted(index.items()))


def attach_command_index(data: dict[str, Any]) -> dict[str, Any]:
    index = build_command_index(data["commands"])
    data["command_index"] = index
    data["stats"]["command_index_names"] = len(index)
    data["stats"]["command_index_multi_section"] = sum(
        1 for entry in index.values() if entry["multi_section"]
    )
    return data


def write_json(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(data: dict[str, Any], path: Path) -> None:
    lines: list[str] = [
        "# CoE5 Modding Manual Rules (extracted)",
        "",
        f"Source: [{data['source_url']}]({data['source_url']})",
        f"Extracted: {data['extracted_at']}",
        "",
        "## Statistics",
        "",
        f"- Sections: {data['stats']['sections']}",
        f"- Commands: {data['stats']['commands']}",
        f"- Reference tables: {data['stats']['reference_tables']}",
        f"- Examples: {data['stats']['examples']}",
    ]
    if "mod_examples" in data:
        lines.append(
            f"- Populum command examples: {data['stats'].get('mod_commands_with_examples', 0)}"
        )
    lines.extend(["", "## Table of Contents", ""])

    for entry in data["table_of_contents"]:
        indent = "  " * entry["depth"]
        lines.append(f"{indent}- [{entry['title']}](#{entry['id']})")

    by_section: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for cmd in sorted(data["commands"], key=lambda item: (item["section_path"], item["name"])):
        by_section.setdefault(tuple(cmd["section_path"]), []).append(cmd)

    lines.extend(["", "## Commands by Section", ""])
    for section_path, cmds in by_section.items():
        lines.append(f"### {' > '.join(section_path)}")
        lines.append("")
        for cmd in cmds:
            lines.append(f"#### `{cmd['syntax']}`")
            lines.append("")
            if cmd["description"]:
                lines.append(cmd["description"])
                lines.append("")
            if cmd.get("see_also"):
                links = ", ".join(f"`{ref}`" for ref in cmd["see_also"])
                lines.append(f"See also: {links}")
                lines.append("")

    if data.get("mod_examples"):
        lines.extend(["## Populum Usage Examples", ""])
        for name in sorted(data["mod_examples"]):
            lines.append(f"### `{name}`")
            lines.append("")
            for sample in data["mod_examples"][name]:
                suffix = f"  # {sample['comment']}" if sample.get("comment") else ""
                lines.append(f"- L{sample['line']}: `{sample['text']}`{suffix}")
            lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_rules(path: Path = DEFAULT_JSON) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(
            f"No extracted rules at {path}. Run: python py_tools/extract_modding_manual.py extract"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_command_index(
    rules_path: Path = DEFAULT_JSON,
    index_path: Path = DEFAULT_INDEX,
) -> dict[str, dict[str, Any]]:
    if index_path.is_file():
        payload = json.loads(index_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and "commands" in payload:
            return payload["commands"]
        return payload

    data = load_rules(rules_path)
    if "command_index" in data:
        return data["command_index"]

    raise SystemExit(
        f"No command index at {index_path}. Run: python py_tools/extract_modding_manual.py extract --command-index"
    )


def cmd_extract(args: argparse.Namespace) -> int:
    html = load_manual_html(cache_path=args.cache, refresh=args.refresh)
    data = parse_manual(html)
    if args.mod:
        data = attach_mod_examples(data, args.mod)
    if args.command_index:
        data = attach_command_index(data)
        index_payload = {
            "source_url": data["source_url"],
            "extracted_at": data["extracted_at"],
            "commands": data["command_index"],
            "stats": {
                "names": data["stats"]["command_index_names"],
                "multi_section": data["stats"]["command_index_multi_section"],
            },
        }
        write_json(index_payload, args.output_index)
    write_json(data, args.output_json)
    if args.output_md:
        write_markdown(data, args.output_md)
    print(f"Wrote {args.output_json} ({data['stats']['commands']} commands)")
    if args.command_index:
        print(
            f"Wrote {args.output_index} "
            f"({data['stats']['command_index_names']} names, "
            f"{data['stats']['command_index_multi_section']} multi-section)"
        )
    if args.output_md:
        print(f"Wrote {args.output_md}")
    return 0


def print_index_entry(name: str, entry: dict[str, Any]) -> None:
    print(f"## {name} ({entry['occurrence_count']} variant(s), {entry['section_count']} section(s))")
    if entry["multi_section"]:
        print("Note: this command appears in multiple manual sections.")
    print()
    for variant in entry["entries"]:
        print(f"### `{variant['syntax']}`")
        print(f"Section: {' > '.join(variant['section_path'])}")
        print()
        print(variant["description"] or "(no description)")
        if variant.get("see_also"):
            print()
            print("See also:", ", ".join(variant["see_also"]))
        print()


def cmd_lookup(args: argparse.Namespace) -> int:
    name = args.command.lower()

    if args.command_index:
        index = load_command_index(args.rules, args.index)
        if name in index:
            print_index_entry(name, index[name])
        else:
            fuzzy = [
                (cmd_name, entry)
                for cmd_name, entry in index.items()
                if name in cmd_name and cmd_name != name
            ]
            if not fuzzy:
                print(f"No command matching {args.command!r}", file=sys.stderr)
                return 1
            for cmd_name, entry in fuzzy:
                print_index_entry(cmd_name, entry)
        data = load_rules(args.rules)
    else:
        data = load_rules(args.rules)
        matches = [cmd for cmd in data["commands"] if cmd["name"] == name]
        if not matches:
            fuzzy = [
                cmd
                for cmd in data["commands"]
                if name in cmd["name"] or name in cmd["syntax"].lower()
            ]
            if not fuzzy:
                print(f"No command matching {args.command!r}", file=sys.stderr)
                return 1
            matches = fuzzy

        for cmd in matches:
            print(f"## {cmd['syntax']}")
            print(f"Section: {' > '.join(cmd['section_path'])}")
            print()
            print(cmd["description"] or "(no description)")
            if cmd.get("see_also"):
                print()
                print("See also:", ", ".join(cmd["see_also"]))
            print()

    if data.get("mod_examples") and name in data["mod_examples"]:
        print("Populum examples:")
        for sample in data["mod_examples"][name]:
            suffix = f"  # {sample['comment']}" if sample.get("comment") else ""
            print(f"  L{sample['line']}: {sample['text']}{suffix}")
        print()

    return 0


def cmd_command_index(args: argparse.Namespace) -> int:
    index = load_command_index(args.rules, args.index)

    if args.name:
        name = args.name.lower()
        if name not in index:
            print(f"No index entry for {args.name!r}", file=sys.stderr)
            return 1
        print_index_entry(name, index[name])
        return 0

    names = sorted(index)
    if args.multi_section:
        names = [name for name in names if index[name]["multi_section"]]

    for name in names[: args.limit]:
        entry = index[name]
        flag = " *" if entry["multi_section"] else ""
        print(
            f"{name}\t{entry['occurrence_count']} variant(s)\t"
            f"{entry['section_count']} section(s){flag}"
        )
    if len(names) > args.limit:
        print(f"... and {len(names) - args.limit} more", file=sys.stderr)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    data = load_rules(args.rules)
    query = args.query.lower()
    hits: list[tuple[str, str, str]] = []

    for cmd in data["commands"]:
        haystack = f"{cmd['syntax']} {cmd['description']} {' '.join(cmd['section_path'])}".lower()
        if query in haystack:
            hits.append((cmd["name"], cmd["syntax"], " > ".join(cmd["section_path"])))

    for table in data["reference_tables"]:
        haystack = f"{table['title']} {table['content']}".lower()
        if query in haystack:
            hits.append((table["id"], table["title"], "reference table"))

    if not hits:
        print(f"No results for {args.query!r}", file=sys.stderr)
        return 1

    for key, label, section in hits[: args.limit]:
        print(f"{key}\t{label}\t[{section}]")
    if len(hits) > args.limit:
        print(f"... and {len(hits) - args.limit} more", file=sys.stderr)
    return 0


def cmd_table(args: argparse.Namespace) -> int:
    data = load_rules(args.rules)
    table_id = args.table_id.lstrip("#")
    matches = [table for table in data["reference_tables"] if table["id"] == table_id]
    if not matches:
        fuzzy = [
            table
            for table in data["reference_tables"]
            if table_id.lower() in table["id"].lower()
            or table_id.lower() in table["title"].lower()
        ]
        if not fuzzy:
            print(f"No reference table matching {args.table_id!r}", file=sys.stderr)
            return 1
        matches = fuzzy

    for table in matches:
        print(f"# {table['title']} ({table['id']})")
        print(f"Section: {' > '.join(table['section_path'])}")
        print()
        print(table["content"])
        print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract", help="Fetch manual and write structured rules")
    extract.add_argument("--refresh", action="store_true", help="Re-download manual HTML")
    extract.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    extract.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    extract.add_argument("--output-md", type=Path, default=DEFAULT_MARKDOWN)
    extract.add_argument("--no-md", action="store_true", help="Skip markdown output")
    extract.add_argument("--mod", type=Path, default=MOD_FILE, help="Attach mod usage examples")
    extract.add_argument("--no-mod", action="store_true", help="Skip mod example scan")
    extract.add_argument(
        "--command-index",
        action="store_true",
        help="Build deduplicated per-name command index (also embedded in JSON)",
    )
    extract.add_argument("--output-index", type=Path, default=DEFAULT_INDEX)
    extract.set_defaults(func=cmd_extract)

    lookup = sub.add_parser("lookup", help="Show manual entry for a command")
    lookup.add_argument("command", help="Command name, e.g. newweapon or gainrit")
    lookup.add_argument("--rules", type=Path, default=DEFAULT_JSON)
    lookup.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    lookup.add_argument(
        "--command-index",
        action="store_true",
        help="Use deduplicated per-name index (recommended for shared command names)",
    )
    lookup.set_defaults(func=cmd_lookup)

    index_cmd = sub.add_parser(
        "command-index",
        help="List or show deduplicated command index",
    )
    index_cmd.add_argument(
        "name",
        nargs="?",
        help="Command name to show; omit to list all indexed names",
    )
    index_cmd.add_argument("--rules", type=Path, default=DEFAULT_JSON)
    index_cmd.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    index_cmd.add_argument(
        "--multi-section",
        action="store_true",
        help="Only list commands that appear in multiple manual sections",
    )
    index_cmd.add_argument("--limit", type=int, default=80)
    index_cmd.set_defaults(func=cmd_command_index)

    search = sub.add_parser("search", help="Search commands and reference tables")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=40)
    search.add_argument("--rules", type=Path, default=DEFAULT_JSON)
    search.set_defaults(func=cmd_search)

    table = sub.add_parser("table", help="Show a reference table from the manual")
    table.add_argument("table_id", help="Table id, e.g. trgrank or dmgtype")
    table.add_argument("--rules", type=Path, default=DEFAULT_JSON)
    table.set_defaults(func=cmd_table)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "extract":
        if args.no_md:
            args.output_md = None
        if args.no_mod:
            args.mod = None

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

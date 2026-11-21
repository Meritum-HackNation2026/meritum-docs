"""Regenerates the generated pages of the docs site; hand-written pages are never touched.

Parts (each optional, each writes only its own files):
  --product-doc  design-system/docs/product-doc.html -> docs/adr/*.md, docs/slownik.md
  --schema       core/contracts/meritum.schema.json  -> docs/referencja/kontrakty.md
  --org          GitHub org (token in GH_TOKEN)      -> docs/architektura/repozytoria.md

Every generated file starts with MARKER, and only files with MARKER are ever deleted.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
MARKER = "<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->"
ADR_RE = re.compile(r"\bADR-(\d{2})\b")


# ---------------------------------------------------------------- product doc -> blocks


class _Blocks(HTMLParser):
    """Flattens the product doc into blocks: ("h", level, md), ("p", md), ("table", head, rows)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple] = []
        self.buf: list[str] | None = None  # inline markdown being collected
        self.inline: list[str] = []  # closing marks for open inline tags
        self.table: dict | None = None
        self.row: list[tuple[str, int]] | None = None
        self.cell_span = 1

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        style = a.get("style") or ""
        if tag in ("h1", "h2", "h3", "p"):
            self.buf = []
        elif tag == "table":
            self.table = {"head": None, "rows": []}
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.buf = []
            self.cell_span = int(a.get("colspan") or 1)
        elif self.buf is None:
            return
        elif tag == "br":
            self.buf.append("<br>")
        elif tag == "strong":
            self.buf.append("**")
            self.inline.append("**")
        elif tag == "em":
            self.buf.append("*")
            self.inline.append("*")
        elif tag == "span":
            mark = "`" if "Mono" in style else ("**" if "#C8213A" in style else "")
            self.buf.append(mark)
            self.inline.append(mark)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("strong", "em", "span") and self.buf is not None and self.inline:
            self.buf.append(self.inline.pop())
        elif tag in ("h1", "h2", "h3") and self.buf is not None:
            self.blocks.append(("h", int(tag[1]), _clean(self.buf)))
            self.buf = None
        elif tag == "p" and self.buf is not None:
            self.blocks.append(("p", _clean(self.buf)))
            self.buf = None
        elif tag in ("td", "th") and self.buf is not None and self.row is not None:
            self.row.append((_clean(self.buf), self.cell_span))
            self.buf = None
        elif tag == "tr" and self.row is not None and self.table is not None:
            if self.table["head"] is None and not self.table["rows"] and self._in_head:
                self.table["head"] = [c for c, _ in self.row]
            else:
                self.table["rows"].append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.blocks.append(("table", self.table["head"], self.table["rows"]))
            self.table = None

    _in_head = False  # set by feed_doc while inside <thead>

    def handle_data(self, data: str) -> None:
        if self.buf is not None:
            self.buf.append(_escape(data))

    def feed_doc(self, html: str) -> list[tuple]:
        # thead marks the header row; tracked with a regex split, simpler than a stack
        for part in re.split(r"(<thead>|</thead>)", html):
            if part == "<thead>":
                self._in_head = True
            elif part == "</thead>":
                self._in_head = False
            else:
                self.feed(part)
        return self.blocks


def _escape(text: str) -> str:
    text = text.replace("​", "")
    return re.sub(r"([\\*_|<>\[\]#`])", r"\\\1", text)


def _clean(parts: list[str]) -> str:
    text = "".join(parts)
    text = re.sub(r"\*\*\s*\*\*|``", "", text)  # empty marks left by empty spans
    return re.sub(r"\s+", " ", text).strip()


def _md_table(head: list[str] | None, rows: list[list[tuple[str, int]]]) -> str:
    width = max([len(head or [])] + [sum(s for _, s in r) for r in rows])
    out: list[str] = []
    if head is None and rows:
        head, rows = [c for c, _ in rows[0]], rows[1:]
    head = (head or []) + [""] * (width - len(head or []))
    out.append("| " + " | ".join(head) + " |")
    out.append("|" + "---|" * width)
    for r in rows:
        if len(r) == 1 and r[0][1] > 1:  # group heading spanning the table
            out.append("| **" + r[0][0].strip("*") + "** |" + " |" * (width - 1))
            continue
        cells = [c for c, _ in r] + [""] * (width - len(r))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def _render(blocks: list[tuple], shift: int = 0) -> str:
    out: list[str] = []
    for b in blocks:
        if b[0] == "h":
            out.append("#" * max(2, b[1] + shift) + " " + b[2])
        elif b[0] == "p":
            out.append(b[1])
        else:
            out.append(_md_table(b[1], b[2]))
    return "\n\n".join(out)


def _render_adr(body: list[tuple]) -> str:
    """The ADR's key-value table (Status, Kontekst, Decyzja, ...) becomes sections; the rest renders as is."""
    first = body[0] if body else None
    if not (first and first[0] == "table" and first[1] is None and all(len(r) == 2 for r in first[2])):
        return _render(body)
    out = []
    for (label, _), (value, _) in first[2]:
        out.append(f"**{label}:** {value.replace('**', '')}" if label == "Status" else f"## {label}\n\n{value}")
    rest = _render(body[1:], shift=-1)
    return "\n\n".join(out + ([rest] if rest else []))


def _link_adrs(text: str, known: set[str], prefix: str) -> str:
    return ADR_RE.sub(lambda m: f"[ADR-{m[1]}]({prefix}adr-{m[1]}.md)" if m[1] in known else m[0], text)


def _sections(blocks: list[tuple]) -> dict[str, list[tuple]]:
    """Groups blocks by their h2 title without the leading number ("4. Decyzje..." -> "Decyzje...")."""
    out: dict[str, list[tuple]] = {}
    current = None
    for b in blocks:
        if b[0] == "h" and b[1] <= 2:
            current = re.sub(r"^\d+\.\s*", "", b[2])
            out[current] = []
        elif current is not None:
            out[current].append(b)
    return out


def write_product_doc(html: str) -> list[Path]:
    secs = _sections(_Blocks().feed_doc(html))
    adr_sec = next((v for k, v in secs.items() if k.startswith("Decyzje architektoniczne")), None)
    glossary = next((v for k, v in secs.items() if k.startswith("Słownik")), None)
    if adr_sec is None or glossary is None:
        sys.exit("product doc: section „Decyzje architektoniczne” or „Słownik” not found")

    intro: list[tuple] = []
    adrs: dict[str, tuple[str, list[tuple]]] = {}
    current: str | None = None
    for b in adr_sec:
        m = re.match(r"ADR-(\d{2})\.\s*(.+)", b[2]) if b[0] == "h" else None
        if m:
            current = m[1]
            adrs[current] = (m[2], [])
        elif current is None:
            intro.append(b)
        else:
            adrs[current][1].append(b)
    if not adrs:
        sys.exit("product doc: no ADR headings found")
    known = set(adrs)

    written: list[Path] = []
    adr_dir = DOCS / "adr"
    adr_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for num, (title, body) in adrs.items():
        status = next((r[1][0] for b in body if b[0] == "table" for r in b[2] if r[0][0] == "Status" and len(r) > 1), "")
        rows.append(f"| [ADR-{num}](adr-{num}.md) | {title} | {status} |")
        page = f"# ADR-{num}. {title}\n\n{MARKER}\n\n" + _link_adrs(_render_adr(body), known, "") + "\n"
        written.append(_write(adr_dir / f"adr-{num}.md", page))
    index = (
        "---\nicon: lucide/scroll-text\n---\n\n# Decyzje architektoniczne (ADR)\n\n"
        f"{MARKER}\n\n"
        + _link_adrs(_render(intro), known, "")
        + "\n\n| Numer | Decyzja | Status |\n|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    written.append(_write(adr_dir / "index.md", index))
    for stale in adr_dir.glob("adr-*.md"):
        if stale not in written and MARKER in stale.read_text(encoding="utf-8"):
            stale.unlink()

    terms: list[str] = []
    for b in glossary:
        if b[0] != "table":
            terms.append(_render([b]))
            continue
        for r in b[2]:
            if len(r) == 1:
                terms.append("## " + r[0][0].strip("*"))
            elif len(r) >= 2:
                term = r[0][0].replace("**", "")
                terms.append(f"{term}\n:   {r[1][0]}")
    glossary_md = "---\nicon: lucide/book-a\n---\n\n# Słownik pojęć\n\n" + MARKER + "\n\n" + "\n\n".join(terms) + "\n"
    written.append(_write(DOCS / "slownik.md", _link_adrs(glossary_md, known, "adr/")))
    return written


# ---------------------------------------------------------------- JSON Schema -> contract reference


def _type(p: dict) -> str:
    if "$ref" in p:
        name = p["$ref"].rsplit("/", 1)[-1]
        return f"[{name}](#{name.lower()})"
    if "enum" in p:
        return " \\| ".join(f"`{v}`" for v in p["enum"])
    if "const" in p:
        return f"`{p['const']}`"
    if "anyOf" in p:
        parts = [_type(x) for x in p["anyOf"]]
        return " \\| ".join(x for x in parts if x != "`null`") + (" \\| `null`" if "`null`" in parts else "")
    t = p.get("type", "")
    if t == "array":
        return f"lista: {_type(p.get('items', {}))}"
    if t == "null":
        return "`null`"
    fmt = f" ({p['format']})" if "format" in p else ""
    return f"`{t}`{fmt}" if t else "dowolny"


def _desc(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").replace("|", "\\|").strip()


def write_schema(schema: dict) -> list[Path]:
    defs = schema.get("$defs", {})
    out = [
        "---\nicon: lucide/braces\n---\n\n# Kontrakty danych\n",
        MARKER,
        f"Wersja kontraktu: `{schema.get('x-contract-version', '?')}`. Źródło prawdy to "
        "`contracts/meritum.schema.json` w meritum-core, generowany z `meritum_core.checks.contracts` "
        "([ADR-02](../adr/adr-02.md)). Opisy pól są po angielsku, tak jak w kodzie.",
        "| Model | Opis |\n|---|---|\n"
        + "\n".join(f"| [{n}](#{n.lower()}) | {_desc(d.get('description')).split('. ')[0]} |" for n, d in defs.items()),
    ]
    for name, d in defs.items():
        out.append(f"## {name}")
        if d.get("description"):
            out.append(_desc(d["description"]))
        if "enum" in d:
            out.append("Wartości: " + ", ".join(f"`{v}`" for v in d["enum"]))
            continue
        req = set(d.get("required", []))
        rows = ["| Pole | Typ | Wymagane | Opis |", "|---|---|---|---|"]
        for field, p in d.get("properties", {}).items():
            rows.append(f"| `{field}` | {_type(p)} | {'tak' if field in req else ''} | {_desc(p.get('description'))} |")
        out.append("\n".join(rows))
    return [_write(DOCS / "referencja" / "kontrakty.md", "\n\n".join(out) + "\n")]


# ---------------------------------------------------------------- GitHub org -> repo map


def write_repos(org: str, token: str) -> list[Path]:
    req = urllib.request.Request(
        f"https://api.github.com/orgs/{org}/repos?per_page=100&type=all",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 - fixed https URL
        repos = sorted(json.load(resp), key=lambda r: r["name"])
    rows = ["| Repozytorium | Opis | Język | Gałąź domyślna |", "|---|---|---|---|"]
    for r in repos:
        if r.get("archived"):
            continue
        desc = _desc(r.get("description")) or ""
        rows.append(f"| [{r['name']}]({r['html_url']}) | {desc} | {r.get('language') or ''} | `{r['default_branch']}` |")
    body = (
        "---\nicon: lucide/folder-git-2\n---\n\n# Mapa repozytoriów\n\n"
        f"{MARKER}\n\n"
        f"Repozytoria organizacji {org} na GitHubie (bez zarchiwizowanych), z opisami z GitHuba. "
        "Co należy do której warstwy, opisuje [Architektura](index.md).\n\n" + "\n".join(rows) + "\n"
    )
    return [_write(DOCS / "architektura" / "repozytoria.md", body)]


def _write(path: Path, text: str) -> Path:
    if path.exists() and MARKER not in path.read_text(encoding="utf-8"):
        sys.exit(f"refusing to overwrite hand-written {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--product-doc", type=Path)
    ap.add_argument("--schema", type=Path)
    ap.add_argument("--org")
    args = ap.parse_args()
    if args.product_doc:
        write_product_doc(args.product_doc.read_text(encoding="utf-8"))
    if args.schema:
        write_schema(json.loads(args.schema.read_text(encoding="utf-8")))
    if args.org:
        token = os.environ.get("GH_TOKEN", "")
        if token:
            write_repos(args.org, token)
        else:
            print("::warning::GH_TOKEN not set, repo map left as is")


if __name__ == "__main__":
    main()

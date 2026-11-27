#!/usr/bin/env python3
"""Convert runbook chapter markdown into collapsible <details> UX (experiment only)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("campaign/prep/arc3-visual-book-ux/chapters")

BANNER = (
    "> **UX-копия** · оригинал не трогаем: "
    "`campaign/prep/arc3-visual-book/`. "
    "Сворачиваемые блоки = `<details>`. "
    "За стол: раскрой **один** бит.\n"
)


def split_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5 :].lstrip("\n")
    return "", text


def wrap_sections(body: str, pattern: str, open_first: bool = False) -> str:
    """Wrap consecutive sections starting with headings matching pattern."""
    lines = body.splitlines(keepends=True)
    heading_re = re.compile(pattern)
    indices = [i for i, ln in enumerate(lines) if heading_re.match(ln)]
    if not indices:
        return body
    out: list[str] = []
    # preamble before first heading
    out.extend(lines[: indices[0]])
    for n, start in enumerate(indices):
        end = indices[n + 1] if n + 1 < len(indices) else len(lines)
        block = lines[start:end]
        title = block[0].lstrip("#").strip()
        # strip trailing blank lines inside for cleanliness
        content = "".join(block[1:])
        while content.startswith("\n"):
            content = content[1:]
        while content.endswith("\n\n\n"):
            content = content[:-1]
        attrs = " open" if (open_first and n == 0) else ""
        out.append(f"<details{attrs}>\n")
        out.append(f"<summary><strong>{title}</strong></summary>\n\n")
        out.append(content.rstrip() + "\n")
        out.append("</details>\n\n")
    return "".join(out)


def ensure_banner(body: str) -> str:
    if "UX-копия" in body[:400]:
        return body
    # after first H1
    m = re.search(r"^# .+$", body, re.M)
    if not m:
        return BANNER + "\n" + body
    insert_at = m.end()
    return body[:insert_at] + "\n\n" + BANNER + body[insert_at:]


def convert_file(path: Path, mode: str) -> None:
    raw = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(raw)
    body = ensure_banner(body)
    if mode == "bits":
        # Wrap ### bits (session door/hub)
        body = wrap_sections(body, r"^### ", open_first=False)
        # Also wrap ## Чеклист if present as details at end — leave open? closed ok
    elif mode == "packs":
        # Wrap top-level # packs except the very first title
        lines = body.splitlines(keepends=True)
        # find all ^#  (single hash) after first
        first = True
        indices = []
        for i, ln in enumerate(lines):
            if re.match(r"^# ", ln):
                if first:
                    first = False
                    continue
                indices.append(i)
        if indices:
            out = lines[: indices[0]]
            for n, start in enumerate(indices):
                end = indices[n + 1] if n + 1 < len(indices) else len(lines)
                block = lines[start:end]
                title = block[0].lstrip("#").strip()
                content = "".join(block[1:]).lstrip("\n")
                out.append("<details>\n")
                out.append(f"<summary><strong>{title}</strong></summary>\n\n")
                out.append(content.rstrip() + "\n")
                out.append("</details>\n\n")
            body = "".join(out)
    elif mode == "banner_only":
        pass
    path.write_text(fm + "\n" + body if fm else body, encoding="utf-8")
    print("converted", path.name, mode)


def main() -> None:
    convert_file(ROOT / "02-sessiya-1-pokhorony.md", "bits")
    for name in [
        "03-dver-a.md",
        "04-dver-f.md",
        "05-dver-d.md",
        "06-dver-e-ldy.md",
        "07-dver-e-mech.md",
        "08-dver-e-sapogi.md",
        "09-dver-b.md",
        "10-dver-c.md",
    ]:
        convert_file(ROOT / name, "bits")
    convert_file(ROOT / "13-vstavki-i-zhertvy.md", "packs")
    for name in [
        "00-kak-vesti.md",
        "01-do-stola.md",
        "11-galereya.md",
        "12-karty.md",
        "14-playbooks-i-side.md",
        "15-spine-posle-s2.md",
        "16-sovet-druidov.md",
    ]:
        convert_file(ROOT / name, "banner_only")
    # gallery: wrap ## NPC cards
    gal = ROOT / "11-galereya.md"
    raw = gal.read_text(encoding="utf-8")
    fm, body = split_frontmatter(raw)
    body = ensure_banner(body)
    # skip wrapping intro ## sections that are meta — wrap ## that have portraits
    body = wrap_sections(body, r"^## (?!Фон|Главные)", open_first=False)
    gal.write_text(fm + "\n" + body if fm else body, encoding="utf-8")
    print("converted gallery cards")


if __name__ == "__main__":
    main()

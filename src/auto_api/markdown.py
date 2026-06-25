from __future__ import annotations

import re

from auto_api.models import ApiDoc


_SLUG_PATTERN = re.compile(r"[^a-z0-9_.-]+")
_DUPLICATE_PATTERN = re.compile(r"^(.*?)-(\d+)$")


def render_markdown(
    docs: list[ApiDoc],
    title: str = "API Documentation",
    include_body: bool = True,
) -> str:
    lines = [f"# {title}", "", "## API reference", ""]

    seen: set[str] = set()
    for doc in docs:
        anchor = _unique_anchor(_entry_label(doc), seen)
        description = doc.description or "No description available."
        lines.append(f"- [{_entry_label(doc)}](#{anchor}) — {description}")
    lines.append("")

    if not include_body:
        return "\n".join(lines).rstrip() + "\n"

    seen = set()
    for doc in docs:
        anchor = _unique_anchor(_entry_label(doc), seen)
        lines.extend(_render_body(doc, anchor))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _entry_label(doc: ApiDoc) -> str:
    return doc.qualified_name or doc.requested_name


def _slugify(name: str) -> str:
    slug = _SLUG_PATTERN.sub("-", name.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def _unique_anchor(name: str, seen: set[str]) -> str:
    base = _slugify(name) or "api"
    if base not in seen:
        seen.add(base)
        return base

    match = _DUPLICATE_PATTERN.match(base)
    if match and match.group(2):
        prefix = match.group(1)
        counter = int(match.group(2))
    else:
        prefix = base
        counter = 1

    while True:
        counter += 1
        candidate = f"{prefix}-{counter}"
        if candidate not in seen:
            seen.add(candidate)
            return candidate


def _render_body(doc: ApiDoc, anchor: str) -> list[str]:
    heading = _entry_label(doc)
    lines = [f'<a id="{anchor}"></a>', f"## {heading}", ""]

    if doc.error:
        lines.extend(
            [
                "Status: unresolved",
                "",
                "Error:",
                "",
                "```text",
                doc.error,
                "```",
            ]
        )
        return lines

    if doc.module:
        lines.extend([f"Source module: `{doc.module}`", ""])

    lines.extend(["Signature:", "", "```python"])
    lines.append(f"{doc.qualified_name}{doc.signature}" if doc.signature else "Signature unavailable")
    lines.extend(["```", "", "Docstring:", "", "```text"])
    lines.append(doc.docstring or "Docstring unavailable")
    lines.append("```")
    return lines

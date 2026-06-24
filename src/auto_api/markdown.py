from __future__ import annotations

from auto_api.models import ApiDoc


def render_markdown(docs: list[ApiDoc], title: str = "API Documentation") -> str:
    lines = [f"# {title}", ""]

    for doc in docs:
        lines.extend(_render_doc(doc))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _render_doc(doc: ApiDoc) -> list[str]:
    heading = doc.qualified_name or doc.requested_name
    lines = [f"## {heading}", ""]

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

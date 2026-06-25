from __future__ import annotations

import inspect

from auto_api.models import ApiDoc, ResolvedApi
from auto_api.resolver import resolve_api, resolve_exposed_apis


def extract_api_doc(target: str, function_name: str) -> ApiDoc:
    try:
        resolved = resolve_api(target, function_name)
    except Exception as exc:
        return ApiDoc(
            requested_name=function_name,
            qualified_name=None,
            module=None,
            signature=None,
            docstring=None,
            description=f"Unresolved: {exc}",
            error=str(exc),
        )

    return extract_resolved_api(resolved)


def extract_resolved_api(resolved: ResolvedApi) -> ApiDoc:
    module = inspect.getmodule(resolved.obj)
    module_name = module.__name__ if module else None

    try:
        signature = str(inspect.signature(resolved.obj))
    except (TypeError, ValueError):
        signature = None

    docstring = inspect.getdoc(resolved.obj)
    return ApiDoc(
        requested_name=resolved.requested_name,
        qualified_name=resolved.qualified_name,
        module=module_name,
        signature=signature,
        docstring=docstring,
        description=first_paragraph(docstring),
    )


def extract_api_docs(target: str, function_names: list[str] | None = None) -> list[ApiDoc]:
    if not function_names:
        try:
            resolved_apis = resolve_exposed_apis(target)
        except Exception as exc:
            return [
                ApiDoc(
                    requested_name=target,
                    qualified_name=None,
                    module=None,
                    signature=None,
                    docstring=None,
                    description=f"Unresolved: {exc}",
                    error=str(exc),
                )
            ]
        return [extract_resolved_api(api) for api in resolved_apis]

    return [extract_api_doc(target, name) for name in function_names]


def first_paragraph(docstring: str | None) -> str | None:
    if not docstring:
        return None
    head = docstring.strip().split("\n\n", 1)[0].strip()
    cleaned = " ".join(head.split())
    return cleaned or None

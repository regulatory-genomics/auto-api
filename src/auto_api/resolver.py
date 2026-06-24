from __future__ import annotations

import importlib
import inspect
import pkgutil
import sys
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Iterator

from auto_api.models import ResolvedApi


@contextmanager
def import_path(target: str) -> Iterator[None]:
    path = Path(target).expanduser()
    if not path.exists():
        yield
        return

    resolved = str(path.resolve())
    sys.path.insert(0, resolved)
    try:
        yield
    finally:
        try:
            sys.path.remove(resolved)
        except ValueError:
            pass


def resolve_api(target: str, function_name: str) -> ResolvedApi:
    with import_path(target):
        candidates = _candidate_paths(target, function_name)
        errors: list[str] = []
        for candidate in candidates:
            try:
                obj, qualified_name = _resolve_dotted_path(candidate)
            except (ImportError, AttributeError) as exc:
                errors.append(f"{candidate}: {exc}")
                continue
            return ResolvedApi(
                requested_name=function_name,
                qualified_name=qualified_name,
                obj=obj,
            )

    detail = "; ".join(errors) if errors else f"No resolution candidates for `{function_name}`."
    raise LookupError(detail)


def resolve_exposed_apis(target: str) -> list[ResolvedApi]:
    with import_path(target):
        path = Path(target).expanduser()
        if path.exists():
            return _resolve_exposed_apis_from_path(path)

        module = importlib.import_module(target)
        return _resolve_exposed_apis_from_module(module)


def _candidate_paths(target: str, function_name: str) -> list[str]:
    if Path(target).expanduser().exists():
        return [function_name]

    if function_name == target or function_name.startswith(f"{target}."):
        return [function_name]

    return [f"{target}.{function_name}", function_name]


def _resolve_exposed_apis_from_path(path: Path) -> list[ResolvedApi]:
    apis: list[ResolvedApi] = []
    for module_info in pkgutil.walk_packages([str(path.resolve())]):
        module = importlib.import_module(module_info.name)
        apis.extend(_resolve_exposed_apis_from_module(module))
    return sorted(apis, key=lambda api: api.qualified_name)


def _resolve_exposed_apis_from_module(module: ModuleType) -> list[ResolvedApi]:
    names = getattr(module, "__all__", None)
    if names is None:
        names = [name for name in dir(module) if not name.startswith("_")]

    apis: list[ResolvedApi] = []
    for name in names:
        try:
            obj = getattr(module, name)
        except AttributeError:
            continue

        if not _is_exposed_function(obj):
            continue

        apis.append(
            ResolvedApi(
                requested_name=f"{module.__name__}.{name}",
                qualified_name=f"{module.__name__}.{name}",
                obj=obj,
            )
        )

    return sorted(apis, key=lambda api: api.qualified_name)


def _is_exposed_function(obj: object) -> bool:
    return inspect.isfunction(obj) or inspect.isbuiltin(obj) or inspect.isroutine(obj)


def _resolve_dotted_path(path: str) -> tuple[object, str]:
    parts = path.split(".")
    if not all(parts):
        raise ImportError(f"Invalid dotted path `{path}`.")

    module, attr_parts = _import_longest_prefix(parts)
    obj: object = module
    qualified_parts = [module.__name__]

    for attr in attr_parts:
        try:
            obj = getattr(obj, attr)
        except AttributeError as exc:
            parent = ".".join(qualified_parts)
            raise AttributeError(f"Could not resolve attribute `{attr}` from `{parent}`.") from exc
        qualified_parts.append(attr)

    return obj, ".".join(qualified_parts)


def _import_longest_prefix(parts: list[str]) -> tuple[ModuleType, list[str]]:
    errors: list[str] = []
    for index in range(len(parts), 0, -1):
        module_name = ".".join(parts[:index])
        try:
            module = importlib.import_module(module_name)
        except ImportError as exc:
            errors.append(f"{module_name}: {exc}")
            continue
        return module, parts[index:]

    raise ImportError("Could not import any module prefix. " + "; ".join(errors))

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ResolvedApi:
    requested_name: str
    qualified_name: str
    obj: Any


@dataclass(frozen=True)
class ApiDoc:
    requested_name: str
    qualified_name: str | None
    module: str | None
    signature: str | None
    docstring: str | None
    error: str | None = None

# auto-api

Extract Python API docstrings and signatures into Markdown that is easy for AI agents to consume.

## Usage

Install dependencies with `uv`:

```bash
uv sync
```

Extract docs from an installed module:

```bash
uv run auto-api extract --target json --functions dumps loads --output api_docs.md
```

Extract docs from a local package by adding a path to `sys.path` during resolution:

```bash
uv run auto-api extract --target ./src --functions my_package.module.function --output api_docs.md
```

Print Markdown to stdout by omitting `--output`:

```bash
uv run auto-api extract --target json --functions dumps loads
```

Output structure (body on):

```md
# API Documentation

## API reference

- [json.dumps](#jsondumps) — Serialize ``obj`` to a JSON formatted ``str``.
- [json.loads](#jsonloads) — Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document) to a Python object.

## json.dumps

Source module: `json`

Signature:

```python
json.dumps(obj, *, skipkeys=False, ...)
```

Docstring:

```text
Serialize ``obj`` to a JSON formatted ``str``.
```
```

Emit only the API reference (no per-entry body) with `--no-body`:

```bash
uv run auto-api extract --target json --no-body
```

Extract all public functions exposed by a target module:

```bash
uv run auto-api extract --target json
```

For installed modules, public functions come from `__all__` when present, otherwise from names that do not start with `_`.

For local filesystem targets, `auto-api` walks importable modules under the path and extracts their public module-level functions:

```bash
uv run auto-api extract --target ./src --output api_docs.md
```

## Notes

- The target module/package is imported, so import-time side effects may occur.
- Docstrings are preserved as cleaned text rather than parsed into a specific style.
- Unresolved APIs are included as error entries by default. Use `--fail-on-error` to return a non-zero exit code when any item fails.

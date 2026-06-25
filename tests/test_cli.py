from pathlib import Path

from auto_api.cli import main


def test_cli_writes_output(tmp_path):
    output = tmp_path / "api.md"

    exit_code = main(["extract", "--target", "json", "--functions", "dumps", "--output", str(output)])

    assert exit_code == 0
    assert "## json.dumps" in output.read_text(encoding="utf-8")


def test_cli_fail_on_error_returns_nonzero(tmp_path):
    output = tmp_path / "api.md"

    exit_code = main(
        [
            "extract",
            "--target",
            "json",
            "--functions",
            "missing",
            "--output",
            str(output),
            "--fail-on-error",
        ]
    )

    assert exit_code == 1
    assert "Status: unresolved" in output.read_text(encoding="utf-8")


def test_cli_extracts_exposed_functions_when_functions_omitted(tmp_path):
    output = tmp_path / "api.md"

    exit_code = main(["extract", "--target", "tests/fixtures", "--output", str(output)])
    markdown = output.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "## sample_lib.documented_function" in markdown
    assert "## sample_lib.undocumented_function" in markdown
    assert "sample_lib._private_function" not in markdown


def test_cli_no_body_skips_per_entry_body(tmp_path):
    output = tmp_path / "api.md"

    exit_code = main(
        [
            "extract",
            "--target",
            "tests/fixtures",
            "--output",
            str(output),
            "--no-body",
        ]
    )
    markdown = output.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "## API reference" in markdown
    assert "## sample_lib.documented_function" not in markdown
    assert "Source module" not in markdown

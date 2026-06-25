from auto_api.markdown import render_markdown
from auto_api.models import ApiDoc


def test_renders_successful_doc():
    markdown = render_markdown(
        [
            ApiDoc(
                requested_name="dumps",
                qualified_name="json.dumps",
                module="json",
                signature="(obj)",
                docstring="Serialize obj.",
                description="Serialize obj.",
            )
        ],
        title="JSON APIs",
    )

    assert "# JSON APIs" in markdown
    assert "## API reference" in markdown
    assert "- json.dumps — Serialize obj." in markdown
    assert "## json.dumps" in markdown
    assert '<a id="json.dumps"></a>' in markdown
    assert "Source module: `json`" in markdown
    assert "json.dumps(obj)" in markdown


def test_renders_unresolved_doc():
    markdown = render_markdown(
        [
            ApiDoc(
                requested_name="missing",
                qualified_name=None,
                module=None,
                signature=None,
                docstring=None,
                description="Unresolved: Could not resolve missing.",
                error="Could not resolve missing.",
            )
        ]
    )

    assert "## API reference" in markdown
    assert "- missing — Unresolved: Could not resolve missing." in markdown
    assert "## missing" in markdown
    assert "Status: unresolved" in markdown
    assert "Could not resolve missing." in markdown


def test_api_reference_only_mode_omits_body():
    markdown = render_markdown(
        [
            ApiDoc(
                requested_name="dumps",
                qualified_name="json.dumps",
                module="json",
                signature="(obj)",
                docstring="Serialize obj.",
                description="Serialize obj.",
            )
        ],
        title="JSON APIs",
        include_body=False,
    )

    assert "## API reference" in markdown
    assert "- json.dumps — Serialize obj." in markdown
    assert "## json.dumps" not in markdown
    assert "Source module" not in markdown


def test_description_uses_first_paragraph_of_docstring():
    markdown = render_markdown(
        [
            ApiDoc(
                requested_name="dumps",
                qualified_name="json.dumps",
                module="json",
                signature="(obj)",
                docstring="Serialize obj.\n\nParameters\n----------\nobj: object",
                description="Serialize obj.",
            )
        ]
    )

    assert "- json.dumps — Serialize obj." in markdown


def test_duplicate_anchors_get_disambiguated():
    markdown = render_markdown(
        [
            ApiDoc(
                requested_name="a",
                qualified_name="pkg.a",
                module="pkg",
                signature="()",
                docstring="First.",
                description="First.",
            ),
            ApiDoc(
                requested_name="A",
                qualified_name="pkg.A",
                module="pkg",
                signature="()",
                docstring="Second.",
                description="Second.",
            ),
        ]
    )

    assert "- pkg.a — First." in markdown
    assert "- pkg.A — Second." in markdown

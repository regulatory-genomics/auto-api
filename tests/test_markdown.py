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
            )
        ],
        title="JSON APIs",
    )

    assert "# JSON APIs" in markdown
    assert "## json.dumps" in markdown
    assert "Source module: `json`" in markdown
    assert "json.dumps(obj)" in markdown
    assert "Serialize obj." in markdown


def test_renders_unresolved_doc():
    markdown = render_markdown(
        [
            ApiDoc(
                requested_name="missing",
                qualified_name=None,
                module=None,
                signature=None,
                docstring=None,
                error="Could not resolve missing.",
            )
        ]
    )

    assert "## missing" in markdown
    assert "Status: unresolved" in markdown
    assert "Could not resolve missing." in markdown

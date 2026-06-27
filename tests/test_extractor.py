from auto_api.extractor import extract_api_doc, extract_api_docs


def test_extracts_signature_and_docstring():
    doc = extract_api_doc("tests/fixtures", "sample_lib.documented_function")

    assert doc.error is None
    assert doc.qualified_name == "sample_lib.documented_function"
    assert doc.signature == "(value: str, repeat: int = 1) -> str"
    assert doc.docstring == "Return ``value`` repeated ``repeat`` times."


def test_handles_missing_docstring():
    doc = extract_api_doc("tests/fixtures", "sample_lib.undocumented_function")

    assert doc.error is None
    assert doc.docstring is None


def test_returns_error_doc_for_unresolved_api():
    doc = extract_api_doc("json", "missing")

    assert doc.error
    assert doc.qualified_name is None


def test_extracts_exposed_api_docs_when_functions_omitted():
    docs = extract_api_docs("tests/fixtures")
    docs_by_name = {doc.qualified_name: doc for doc in docs}

    assert "fixtures.sample_lib.documented_function" in docs_by_name
    assert "fixtures.sample_lib.undocumented_function" in docs_by_name
    assert docs_by_name["fixtures.sample_lib.SampleClass"].docstring == "Represent a documented sample class."

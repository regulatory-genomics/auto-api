from auto_api.resolver import resolve_api, resolve_exposed_apis


def test_resolves_stdlib_function_relative_to_target():
    resolved = resolve_api("json", "dumps")

    assert resolved.qualified_name == "json.dumps"
    assert callable(resolved.obj)


def test_resolves_stdlib_function_with_fully_qualified_path():
    resolved = resolve_api("json", "json.loads")

    assert resolved.qualified_name == "json.loads"
    assert callable(resolved.obj)


def test_resolves_class_method_from_local_path():
    resolved = resolve_api("tests/fixtures", "sample_lib.SampleClass.method")

    assert resolved.qualified_name == "sample_lib.SampleClass.method"
    assert callable(resolved.obj)


def test_missing_object_raises_lookup_error():
    try:
        resolve_api("json", "missing")
    except LookupError as exc:
        assert "missing" in str(exc)
    else:
        raise AssertionError("Expected LookupError")


def test_resolves_exposed_functions_from_module_target():
    resolved = resolve_exposed_apis("json")
    names = {api.qualified_name for api in resolved}

    assert "json.dumps" in names
    assert "json.loads" in names


def test_resolves_exposed_functions_from_local_path():
    resolved = resolve_exposed_apis("tests/fixtures")
    names = {api.qualified_name for api in resolved}

    assert "fixtures.sample_lib.documented_function" in names
    assert "fixtures.sample_lib.undocumented_function" in names
    assert "fixtures.sample_lib.SampleClass" in names
    assert "fixtures.sample_lib._private_function" not in names


def test_resolves_exposed_submodules_from_local_path():
    resolved = resolve_exposed_apis("tests/fixtures/sample_pkg")
    names = {api.qualified_name for api in resolved}

    assert "sample_pkg.helpers.helper_function" in names
    assert "sample_pkg.nested.deep.deep_function" in names
    assert "sample_pkg._internal.internal_function" not in names


def test_include_private_submodules_flag_includes_private():
    resolved = resolve_exposed_apis(
        "tests/fixtures/sample_pkg",
        include_private_submodules=True,
    )
    names = {api.qualified_name for api in resolved}

    assert "sample_pkg._internal.internal_function" in names


def test_dedupe_when_name_appears_in_submodule_and_reexport():
    from tests.fixtures import sample_pkg
    from tests.fixtures.sample_pkg import helpers

    sample_pkg.helper_function = helpers.helper_function
    try:
        resolved = resolve_exposed_apis("tests/fixtures/sample_pkg")
        helper_entries = [
            api
            for api in resolved
            if api.qualified_name.endswith(".helper_function")
        ]
        assert len(helper_entries) == 1
    finally:
        del sample_pkg.helper_function

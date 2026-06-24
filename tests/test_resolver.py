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

    assert "sample_lib.documented_function" in names
    assert "sample_lib.undocumented_function" in names
    assert "sample_lib._private_function" not in names

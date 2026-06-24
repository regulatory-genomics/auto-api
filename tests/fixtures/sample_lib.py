def documented_function(value: str, repeat: int = 1) -> str:
    """Return ``value`` repeated ``repeat`` times."""
    return value * repeat


def undocumented_function(value):
    return value


def _private_function():
    return None


class SampleClass:
    def method(self, number: int) -> int:
        """Return ``number`` unchanged."""
        return number

"""Backend Utils Module — General-purpose helper stubs."""


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    return text.lower().replace(" ", "-")


def truncate(text: str, max_len: int = 100) -> str:
    """Truncate text to max_len characters."""
    return text[:max_len] + "..." if len(text) > max_len else text

import toml

def version_str() -> str:
    """
    Gets the version of Open-Bus API from its metadata.

    Returns: Version string
    """
    with open("pyproject.toml") as f:
        data = toml.load(f)

    return data["project"]["version"]

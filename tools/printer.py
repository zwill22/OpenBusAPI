def print_config(name, value, newline: bool = False, **kwargs):
    """
    Print formatted configuration value
    Args:
        name (): Configuration name
        value (): Configuration value
        newline (bool): Include newline before printing
        **kwargs (): Additional keyword arguments

    Returns:

    """
    if len(name) > 32:
        raise ValueError("Config name `{}` is too long".format(name))
    if newline:
        print()
    print("{0:32} {1}".format(name, value), **kwargs)

def print_config(name, value, newline=False, **kwargs):
    if len(name) > 32:
        raise ValueError("Config name `{}` is too long".format(name))
    if newline:
        print()
    print("{0:32} {1}".format(name, value), **kwargs)

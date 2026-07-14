import argparse


def parse_cmdline(args=None) -> argparse.Namespace:
    """
    Parse commandline arguments and return an argparse.Namespace

    Args:
        args (list, optional): Arguments to parse directly

    Returns: Argparse Namespace
    """

    parser = argparse.ArgumentParser(
        prog="OpenBusAPI",
        description="""
        Welcome to the OpenBusAPI which provides an interface to bus data for the
        BusTracker App. All configuration options should be passed via the config file.
        """,
        epilog="Diolch yn fawr iawn.",
    )

    parser.add_argument(
        "config_file",
        help="Filepath for config file (default: config.json)",
        nargs="?",
        default="config.json",
    )

    return parser.parse_args(args=args)

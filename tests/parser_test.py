from open_bus_api.parser import parse_cmdline


def test_parser():
    args = parse_cmdline(args=[])

    assert args.config_file == "config.json"

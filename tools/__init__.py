from pathlib import Path

from .location_tools import get_base_url as get_base_url
from .location_tools import get_location_url as get_location_url
from .output import api_output as api_output
from .version import version_str as version_str


def get_root():
    return Path(__file__).parent.parent.absolute()

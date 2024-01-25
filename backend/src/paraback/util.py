import logging
from pathlib import Path
from typing import Any, Dict, Union

import yaml

from pathlib import Path
from contextlib import contextmanager
import os
import sys

logger = logging.getLogger('paraback')


def load_config(config_file: Union[str, Path]) -> Dict[str, Any]:
    """
    Load the config from the specified yaml file

    :param config_file: path of the config file to load
    :return: the parsed config as dictionary
    """
    with open(config_file, 'r') as fp:
        return yaml.safe_load(fp)


def logging_setup(config: Dict):
    """
    setup logging based on the configuration

    :param config: the parsed config tree
    """
    log_conf = config['logging']
    fmt = log_conf['format']
    if log_conf['enabled']:
        level = logging._nameToLevel[log_conf['level'].upper()]
    else:
        level = logging.NOTSET
    logging.basicConfig(format=fmt, level=level)
    logger.setLevel(level)



@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_sterr = sys.stderr
        sys.stderr = devnull
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_sterr


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def get_data_path() -> Path:
    return get_project_root() / "data"

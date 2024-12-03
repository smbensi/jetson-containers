import platform
import os

from pathlib import Path


def is_docker() -> bool:
    """
    Determine if the script is running inside a Docker container

    Returns:
        bool: True if the script is running inside a Docker container, False otherwise
    """
    if os.path.exists("/.dockerenv"):
        return True
    # with contextlib.suppress(Exception):
    #     with open("/proc/self/cgroup") as f:
    #         return "docker" in f.read()
    return False


def set_logger():
    if is_docker():
        import xtendlog
        try:
            logger = xtendlog.loggerclass.get()
        except AttributeError:
            module = 'object detection'
            logger = xtendlog.loggerclass.create(f'{module}')
    else:
        import logging
        logger = logging.getLogger(__name__)
        # Set the logging level
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        
        # # Add the handlers to the logger
        logger.addHandler(stream_handler)
        
    return logger


LOGGER = set_logger()
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
ROOT_PARENT = ROOT.parents[0]
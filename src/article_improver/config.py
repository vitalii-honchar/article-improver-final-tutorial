import asyncio
import sys
import yaml
from dataclasses import dataclass
from loguru import logger
import os

DEFAULT_CONFIG_FILE_FOLDER = f"{os.path.expanduser('~')}/.config/articleimprover"
DEFAULT_CONFIG_FILE = "config.yaml"

FIELD_OPEN_AI_KEY = "open_ai_key"


@dataclass
class Config:
    open_ai_key: str


def _read_config(config_file_folder: str, config_file: str) -> Config:

    if config_file_folder is None or config_file is None:
        file = f"{DEFAULT_CONFIG_FILE_FOLDER}/{DEFAULT_CONFIG_FILE}"
    else:
        file = f"{config_file_folder}/{config_file}"

    with open(file) as f:
        config_json = yaml.safe_load(f)
        return Config(config_json[FIELD_OPEN_AI_KEY])


def init(
    config_file_folder: str = None, config_file: str = None
) -> tuple[Config, asyncio.AbstractEventLoop]:
    logger.remove()
    logger.add(sys.stderr, format="{message}", level="INFO")
    try:
        cfg = _read_config(config_file_folder, config_file)
    except:
        print("No valid configuration file!")
        cfg = None
    return (cfg, asyncio.get_event_loop_policy().get_event_loop())

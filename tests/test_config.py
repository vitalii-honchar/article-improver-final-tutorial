from article_improver import config
from uuid import uuid4
import os


def test_return_config_if_file_exists():
    # GIVEN
    folder = "tests"
    filename = "test_config.yaml"
    expected_open_ai_key = "test-key"

    # WHEN
    cfg, loop = config.init(folder, filename)

    # THEN
    assert loop is not None
    assert cfg is not None
    assert cfg.open_ai_key == expected_open_ai_key


def test_return_none_if_file_not_exists():
    # GIVEN
    folder = str(uuid4())
    filename = f"{str(uuid4())}.yaml"

    # WHEN
    cfg, loop = config.init(folder, filename)

    # THEN
    assert loop is not None
    assert cfg is None


def test_default_config_file_folder():
    # GIVEN
    expected = f"{os.path.expanduser('~')}/.config/articleimprover"

    # WHEN-THEN
    assert config.DEFAULT_CONFIG_FILE_FOLDER == expected


def test_default_config_file():
    # GIVEN
    expected = "config.yaml"

    # WHEN-THEN
    assert config.DEFAULT_CONFIG_FILE == expected

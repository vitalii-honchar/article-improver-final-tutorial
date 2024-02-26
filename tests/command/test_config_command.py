import pytest
import shutil
import yaml
from pathlib import Path
from uuid import uuid4
from article_improver.command import config_command


@pytest.fixture
def not_exists_folder():
    folder = str(uuid4())
    yield folder
    shutil.rmtree(folder)


@pytest.fixture
def exists_folder():
    folder = str(uuid4())
    Path(folder).mkdir(parents=True, exist_ok=True)
    yield folder
    shutil.rmtree(folder)


@pytest.fixture(params=["not_exists_folder", "exists_folder"])
def folder_fixture(request):
    if request.param == "not_exists_folder":
        folder = request.getfixturevalue("not_exists_folder")
    else:
        folder = request.getfixturevalue("exists_folder")
    yield folder


@pytest.fixture
def exists_file(exists_folder):
    filename = str(uuid4()) + ".yaml"
    with open(f"{exists_folder}/{filename}", "w") as f:
        yaml.dump({}, f)

    yield filename
    Path(f"{exists_folder}/{filename}").unlink(missing_ok=True)


def test_create_file_if_folder_not_exists(monkeypatch, folder_fixture):
    # GIVEN
    filename = str(uuid4()) + ".yaml"
    token = str(uuid4())
    expected_file = f"{folder_fixture}/{filename}"

    monkeypatch.setattr("builtins.input", lambda _: token)

    # WHEN
    config_command.handle(filename, folder_fixture)

    # THEN
    assert Path(expected_file).exists()

    with open(expected_file) as f:
        config_json = yaml.safe_load(f)
        assert config_json["open_ai_key"] == token


def test_rewrite_file_if_file_exists(monkeypatch, exists_file, exists_folder):
    # GIVEN
    token = str(uuid4())
    expected_file = f"{exists_folder}/{exists_file}"

    monkeypatch.setattr("builtins.input", lambda _: token)

    # WHEN
    config_command.handle(exists_file, exists_folder)

    # THEN
    assert Path(expected_file).exists()

    with open(expected_file) as f:
        config_json = yaml.safe_load(f)
        assert config_json["open_ai_key"] == token

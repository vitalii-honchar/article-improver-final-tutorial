from article_improver.config import FIELD_OPEN_AI_KEY
from pathlib import Path
import yaml


def handle(filename: str, folder: str):
    print("Generating new config file...")
    token = input("Please, enter OpenAI token: ")
    cfg_file = f"{folder}/{filename}"
    Path(folder).mkdir(parents=True, exist_ok=True)
    cfg = {FIELD_OPEN_AI_KEY: token}
    with open(cfg_file, "w") as f:
        yaml.dump(cfg, f)
    print(f"New config file has generated: {cfg_file}")

from pathlib import Path

BASE_DIR = Path(__file__).absolute().resolve().parents[1]

CONFIG_FILE = BASE_DIR / "config.yml"

FILES_DIR = BASE_DIR / "files"
SHARES_DIR = BASE_DIR / "shares"
PARAMS_DIR = BASE_DIR / "params"
KEYS_DIR = BASE_DIR / "keys"
IVS_DIR = BASE_DIR / "ivs"

DEFAULT_FILE = FILES_DIR / "default.txt"

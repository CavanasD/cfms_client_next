__all__ = ["global_config"]

import os
import secrets
import tomllib

from tomlkit import dumps, parse

from include.constants import ROOT_ABSPATH

# include/conf_loader.py

# This module loads the global configuration from a TOML file.
# It is intended to be imported by other modules to access the configuration settings.
# Load the global configuration from a TOML file.

# Ensure that the file is read in binary mode for compatibility with tomllib

if __name__ == "__main__":
    raise RuntimeError("This module should not be run directly.")

config_path = ROOT_ABSPATH / "config.toml"
init_path = ROOT_ABSPATH / "init"

if not os.path.exists(config_path):
    raise FileNotFoundError("Configuration file 'config.toml' not found.")

with open(config_path, "rb") as f:
    global_config = tomllib.load(f)

for section_name, key_name in (
    ("server", "ssl_keyfile"),
    ("server", "ssl_certfile"),
    ("security", "client_cert_ca_path"),
    ("database", "file"),
):
    section = global_config.get(section_name)
    if not isinstance(section, dict):
        continue

    value = section.get(key_name)
    if isinstance(value, str) and value and not os.path.isabs(value):
        section[key_name] = ROOT_ABSPATH / value

if not os.path.exists(init_path):
    with open(config_path, "r", encoding="utf-8") as f:
        toml_doc = parse(f.read())

    secret_key = secrets.token_hex(32)
    toml_doc["server"]["secret_key"] = secret_key  # type: ignore

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(dumps(toml_doc))

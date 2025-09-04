import os
import sys
from dynaconf import Dynaconf
from logger_config import logger

# Determine root_path based on platform and environment
if sys.platform == "win32":
    # On Windows, use APPDATA directory
    root_path = os.path.join(os.environ.get("APPDATA", ""), "ledmonitor")
else:
    # On other platforms, use home directory
    root_path = os.path.join(os.path.expanduser("~"), ".ledmonitor")

# Check if config file exists in root_path, otherwise use current directory
config_file_path = os.path.join(root_path, "config.toml")
if not os.path.exists(root_path):
    root_path = "./config"

logger.info(f"Using config file: {config_file_path}, {root_path}")
settings = Dynaconf(
    root_path=root_path,
    envvar_prefix="DYNACONF",
    settings_files=["config.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

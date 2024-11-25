"""
Get the configuration using Hydra and store it in a global variable.
This function initializes the configuration based on the specified config path and name.

Args:
    cfg (DictConfig): The configuration object loaded by Hydra.

Returns:
    None

Raises:
    None

Examples:
    To run the configuration loading, execute the script directly.
"""

import os

from hydra import initialize, compose
from omegaconf import DictConfig, OmegaConf

initialize(version_base="1.3.2", config_path="conf")


# pylint: disable=W0603

def get_config() -> DictConfig:
  """
  Get the configuration using Hydra and store it in a global variable.

  Args:
      cfg (DictConfig): The configuration object loaded by Hydra.

  Returns:
      None

  Raises:
      None

  Examples:
      To run the configuration loading, execute the script directly.
  """

  cfg = compose(config_name="config")
  print(OmegaConf.to_yaml(cfg))
  return cfg


CONFIG = get_config()
print(CONFIG)

if __name__ == "__main__":
  # os.environ["HYDRA_FULL_ERROR"] = "1"
  os.environ["APP_ENV"] = "unittest"
  get_config()
  del os.environ["APP_ENV"]
  get_config()

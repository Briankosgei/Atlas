from pathlib import Path
import yaml


class ConfigManager:
    """
    Central configuration manager for AtlasTrader.
    Loads all YAML configuration files.
    """

    def __init__(self):
        self.config_dir = Path("config")

    def _load_yaml(self, filename):
        """Load a YAML file."""

        file_path = self.config_dir / filename

        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def get_symbols(self):
        return self._load_yaml("symbols.yaml")

    def get_risk(self):
        return self._load_yaml("risk.yaml")

    def get_strategy(self):
        return self._load_yaml("strategy.yaml")

    def get_sessions(self):
        return self._load_yaml("sessions.yaml")
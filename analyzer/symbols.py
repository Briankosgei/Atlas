from pathlib import Path
import yaml


class SymbolManager:
    """
    Loads all trading symbols from config/symbols.yaml
    """

    def __init__(self):
        self.config_path = Path("config/symbols.yaml")
        self.symbols = []

    def load(self):
        """Load symbols from YAML configuration."""

        with open(self.config_path, "r") as file:
            data = yaml.safe_load(file)

        self.symbols = data["symbols"]
        return self.symbols

    def enabled_symbols(self):
        """Return only enabled symbols."""

        return [
            symbol
            for symbol in self.symbols
            if symbol.get("enabled", False)
        ]


if __name__ == "__main__":

    manager = SymbolManager()

    manager.load()

    print("\nConfigured Symbols\n")

    for symbol in manager.enabled_symbols():
        print(symbol["name"])
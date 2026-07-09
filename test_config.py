from config.config_manager import ConfigManager

config = ConfigManager()

print("\n===== SYMBOLS =====")
print(config.get_symbols())

print("\n===== RISK =====")
print(config.get_risk())

print("\n===== STRATEGY =====")
print(config.get_strategy())

print("\n===== SESSIONS =====")
print(config.get_sessions())
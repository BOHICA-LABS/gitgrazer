import os
import json
from abc import ABCMeta, abstractmethod


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigBase(metaclass=Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_configuration(self):
        pass


class AppConfig(ConfigBase):
    CONFIGS = {}

    def __init__(self, config_file='config.json',
                 config_keys=['OPENAI_API_KEY']):  # Add the keys of additional configurations here
        self.config_file = config_file
        self.config_keys = config_keys

    def load_configuration(self):
        for key in self.config_keys:
            env_value = os.getenv(key)
            if env_value:
                self.CONFIGS[key] = env_value
            else:
                try:
                    with open(self.config_file, 'r') as f:
                        config_data = json.load(f)
                        if key in config_data:
                            self.CONFIGS[key] = config_data.get(key)
                        else:
                            print(f"No value found for {key} in environment variables or config file")
                except FileNotFoundError:
                    print(f'Config file "{self.config_file}" not found, and {key} env var not set')
                    break

    def get_config_value(self, key):
        return self.CONFIGS.get(key, None)


class ConfigManager:
    def __init__(self):
        self.app_config = AppConfig()
        self.app_config.load_configuration()

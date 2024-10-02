#- plugin_manager.py -#

import os
import importlib
from log import Log

class PluginManager:
    def __init__(self, main_window, plugin_dir="plugins"):
        self.log = Log()
        self.main_window = main_window 
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py"):
                plugin_name = filename[:-3]
                try:
                    module = importlib.import_module(f"{self.plugin_dir}.{plugin_name}")
                    if hasattr(module, 'load'):
                        module.load(self.main_window)
                        self.plugins.append(module)
                        self.log.info(f"Plugin '{plugin_name}' loaded.")
                    else:
                        self.log.info(f"Plugin '{plugin_name}' does not have a load(window) function.")
                except Exception as e:
                    self.log.info(f"Error loading plugin '{plugin_name}': {e}")

    def get_plugins(self):
        return self.plugins

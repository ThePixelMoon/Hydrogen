#- plugin_manager.py -#

import os
import importlib

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py"):
                plugin_name = filename[:-3]
                try:
                    module = importlib.import_module(f"{self.plugin_dir}.{plugin_name}")
                    if hasattr(module, 'load'):
                        module.load()
                        self.plugins.append(module)
                        print(f"Plugin '{plugin_name}' loaded.")
                    else:
                        print(f"Plugin '{plugin_name}' does not have a load() function.")
                except Exception as e:
                    print(f"Error loading plugin '{plugin_name}': {e}")

    def get_plugins(self):
        return self.plugins

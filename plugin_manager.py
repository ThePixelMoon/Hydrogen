#- plugin_manager.py -#

import os, importlib, json
from log import Log

class PluginManager:
    def __init__(self, main_window, plugin_dir="plugins"):
        self.log = Log()
        self.main_window = main_window 
        self.plugin_dir = plugin_dir
        self.plugins = []
        self.language = "en" # default
        self.translations = self.load_translations()

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py"):
                plugin_name = filename[:-3]
                try:
                    module = importlib.import_module(f"{self.plugin_dir}.{plugin_name}")
                    if hasattr(module, 'load'):
                        module.load(self.main_window)
                        self.plugins.append(module)
                        self.log.info(f"{self.translate("plugin")} '{plugin_name}' {self.translate("loaded")}")
                    else:
                        self.log.info(f"{self.translate("plugin")} '{plugin_name}' {self.translate("plugin_no_function")}")
                except Exception as e:
                    self.log.info(f"{self.translate("error_loading_plugin")} '{plugin_name}': {e}")

    def load_translations(self):
        try:
            with open(f"translations/{self.language}.json", "r", encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def translate(self, key):
        return self.translations.get(self.language, {}).get(key, key)

    def get_plugins(self):
        return self.plugins

import json
import os

class Settings:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.settings = {
            "theme": "themes/default.eft",
        }
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_theme(self):
        return self.settings["theme"]

    def set_theme(self, theme_path):
        self.settings["theme"] = theme_path
        self.save_settings()

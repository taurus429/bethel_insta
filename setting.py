import json
import os

SETTINGS_FILE = "settings.json"


class Setting:

    def __init__(self):
        self.settings = None
        self.load_settings()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as file:
                self.settings = json.load(file)
        else:
            # 기본 설정 파일 생성
            self.settings = {
                "birthday_file": None,
            }
            self.save_settings(self.settings)

    def set_settings(self, key, data):
        self.settings[key] = data
        self.save_settings(self.settings)

    def get_settings(self, key):
        if key in self.settings.keys():
            return self.settings[key]
        else:
            return None

    def save_settings(self, settings):
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(settings, file, indent=4)

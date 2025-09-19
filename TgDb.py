import json
import os

class TelegramDB:
    def __init__(self, filename):
        self.filename = filename

    def set_value(self, telegram_id, name, value):
        data = self.get_data()
        str_id = str(telegram_id)
        if str_id not in data:
            data[str_id] = {}
        data[str_id][name] = value
        self.save_data(data)

    def get_value(self, telegram_id, name):
        data = self.get_data()
        str_id = str(telegram_id)
        if str_id not in data:
            return None
        return data[str_id].get(name)

    def get_data(self):
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_data(self, data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

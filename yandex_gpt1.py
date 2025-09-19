import requests

class YandexGPT:
    def __init__(self):
        self.token = ""  # твой API-ключ
        self.catalog = ""  # твой catalogId
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def get_answer(self, messages):
        data = {
            "modelUri": f"gpt://{self.catalog}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.4,
                "maxTokens": 200
            },
            "messages": messages
        }

        headers = {"Authorization": f"Api-key {self.token}"}
        response = requests.post(self.url, json=data, headers=headers)
        result = response.json()
        print("DEBUG:", result)  # можно оставить для проверки

        if "result" in result:
            return result['result']['alternatives'][0]['message']['text']
        elif "error" in result:
            err = result["error"]
            if isinstance(err, dict):
                return f"Ошибка от Яндекс GPT: {err.get('message', 'неизвестно')}"
            else:
                return f"Ошибка от Яндекс GPT: {err}"
        else:
            return "Не удалось получить ответ от Яндекс GPT"

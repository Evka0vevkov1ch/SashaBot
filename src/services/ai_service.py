import requests, logging
class AIService:
    def __init__(self, api_key):
        self.api_key = api_key

    async def get_ai_response(self, text):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        json_data = {
            "model": "mistralai/mixtral-8x7b-instruct",
            "messages": [
                {"role": "system", "content": (
                    "Ты переводчик с непонятного языка на нормальный русский. "
                    "Отвечай только на русском языке. "
                    "Переводи суть кратко, без пояснений и анализа."
                )},
                {"role": "user", "content": f"Переведи на нормальный русский:\n{text}"}
            ],
            "temperature": 0.1  
        }

        try:
            response = requests.post(url, headers=headers, json=json_data)
            response_json = response.json()
            ai_text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

            if not ai_text:
                logging.warning("⚠️ OpenRouter вернул пустой ответ")
                return "Я не понял, что он сказал 🤷‍♂️"

            return ai_text
        except Exception as e:
            logging.error(f"❌ Ошибка AI: {e}")
            return "Ошибка AI, попробуй позже!"
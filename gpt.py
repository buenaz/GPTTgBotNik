import requests
from transformers import AutoTokenizer
import config
import sqlite3

MAX_LENGTH = 512

tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME)

def generate_response(question):
    inputs = tokenizer.encode(question, add_special_tokens=False, return_tensors='pt')
    input_length = inputs.size()[1]
    if input_length > MAX_LENGTH:
        return 'Ошибка: ваш вопрос слишком длинный. Пожалуйста, сократите его.'
    response = requests.post(
        config.API_URL,
        headers={"Content-Type": "application/json"},

        json={
            "messages": [
                {"role": "system", "content": config.system_content},
                {"role": "user", "content": question},
            ],
            "temperature": 1,
            "max_tokens": 512
        }
    )
    if response.status_code == 200 and 'choices' in response.json():
        return response.json()['choices'][0]['message']['content']
    else:
        return 'Не удалось получить ответ от нейросети'


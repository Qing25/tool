import openai
import os 

model = "gpt-4o-mini"

client = openai.OpenAI(
        api_key=os.environ.get('CHATANY_API_KEY'),
        base_url="https://api.chatanywhere.tech/v1",
    )

import openai
from config import load_config

def get_openai_client():
    config = load_config()
    openai.api_key = config["openai_api_key"]
    return openai

def get_embedding(text):
    openai_client = get_openai_client()
    config = load_config()
    response = openai_client.Embedding.create(
        input=text,
        model=config["embedding_model"]
    )
    return response['data'][0]['embedding']

def ask_gpt(context, question):
    openai_client = get_openai_client()
    config = load_config()
    prompt = f"请参考以下资料回答问题：\n{context}\n\n问题：{question}"
    response = openai_client.ChatCompletion.create(
        model=config["chat_model"],
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
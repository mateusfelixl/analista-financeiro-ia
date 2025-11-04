
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv(override=True)

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Chave carregada: {api_key[:20]}...")  # Mostra só o começo

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content("Diga olá")
print(f"✅ Resposta: {response.text}")

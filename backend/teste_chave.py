import os
import google.generativeai as genai
from dotenv import load_dotenv

def carregar_configuracoes():
    """
    Carrega as variáveis de ambiente do arquivo .env.
    """
    load_dotenv(override=True)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERRO: GOOGLE_API_KEY não encontrada no arquivo .env.")
        return None
    
    print(f"🔑 Chave API carregada com sucesso (começa com: {api_key[:4]}...)")
    return api_key

def testar_conexao_gemini(api_key: str):
    """
    Tenta configurar a API e fazer uma chamada de teste simples.
    """
    try:
        genai.configure(api_key=api_key)
        
        print("\n⚙️  Inicializando o modelo (gemini-2.5-flash)...")
        # Configurações de segurança leves para o teste
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        ]
        model = genai.GenerativeModel("gemini-2.5-flash", safety_settings=safety_settings)

        print("🚀 Enviando requisição de teste ('Quem é você?')...")
        response = model.generate_content("Quem é você em uma frase?")
        
        print("\n--- SUCESSO! ---")
        print(f"✅ Resposta da IA: {response.text.strip()}")
        print("--------------------")

    except Exception as e:
        print("\n--- 🛑 FALHA NO TESTE 🛑 ---")
        print(f"Ocorreu um erro ao tentar conectar com a API do Google:")
        print(f"{e}")
        print("-------------------------")
        print("Dicas:")
        print("1. Verifique se a API Key está correta e se a API 'Generative Language' está ativada no seu painel do Google Cloud.")
        print("2. Verifique se o faturamento (billing) está ativado na sua conta Google.")

def main():
    """
    Função principal para executar o diagnóstico.
    """
    print("--- Iniciando Diagnóstico de Conexão (teste_chave.py) ---")
    api_key = carregar_configuracoes()
    
    if api_key:
        testar_conexao_gemini(api_key)

# Este bloco padrão do Python garante que o 'main()' só rode
# quando você executa o script diretamente.
if __name__ == "__main__":
    main()
import os
from dotenv import load_dotenv

def test_environment():
    load_dotenv(override=True)
    
    print("--- Teste de Variáveis de Ambiente ---")
    
    google = os.getenv("GOOGLE_API_KEY")
    serper = os.getenv("SERPER_API_KEY")
    
    if google:
        print(f"✅ GOOGLE_API_KEY encontrada: {google[:5]}...******")
    else:
        print("❌ GOOGLE_API_KEY não encontrada!")

    if serper:
        print(f"✅ SERPER_API_KEY encontrada: {serper[:5]}...******")
    else:
        print("❌ SERPER_API_KEY não encontrada!")

if __name__ == "__main__":
    test_environment()
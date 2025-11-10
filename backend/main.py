# --- main.py (A Nova Versão) ---
import uvicorn
import traceback
from fastapi import FastAPI, HTTPException, Depends
from starlette.concurrency import run_in_threadpool

# Importações locais dos nossos novos arquivos
from models import StockAnalysisRequest, AnalysisResponse
from rate_limiter import check_rate_limit
from crew_service import crew_service # Importa a INSTÂNCIA ÚNICA

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Servidor 'Cérebro' (Python/FastAPI) está online.", "version": "3.0.0-refactored"}

@app.post("/analyze-stock", response_model=AnalysisResponse)
async def analyze_stock(
    # 1. Valida o body da requisição usando o Pydantic Model
    request_data: StockAnalysisRequest,
    
    # 2. Executa o rate limiter. Se falhar, nem entra na função.
    _ = Depends(check_rate_limit) 
):
    
    if crew_service is None:
        raise HTTPException(status_code=500, detail="ERRO CRÍTICO: O serviço de IA falhou ao inicializar. Verifique os logs e as API Keys.")
        
    try:
        print(f"\n--- REQUISIÇÃO RECEBIDA: Analisando {request_data.stock_symbol} ---")
        
        # --- 3. Roda a função síncrona (pesada) do crew em uma threadpool ---
        result_data = await run_in_threadpool(
            crew_service.run_analysis, 
            request_data.stock_symbol
        )
        
        # --- 4. Retorna os dados validados pelo Pydantic ---
        return AnalysisResponse(**result_data)

    except Exception as e:
        error_message = str(e)
        print(f"--- 🛑 ERRO CRÍTICO NO main.py 🛑 ---")
        print(f"Erro: {error_message}")
        traceback.print_exc()
        
        if "rate_limit" in error_message.lower() or "quota" in error_message.lower():
             raise HTTPException(status_code=429, detail={"message": "API do Google atingiu o limite de taxa (quota). Aguarde 60 segundos.", "wait_seconds": 60})
        
        raise HTTPException(status_code=500, detail=f"ERRO INTERNO NO PYTHON: {error_message}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
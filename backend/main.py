import time
import uvicorn
import traceback
from fastapi import FastAPI, HTTPException
from starlette.concurrency import run_in_threadpool

# Imports
from config import Config
from schemas import StockAnalysisRequest, StockAnalysisResponse
from crew_service import FinancialAnalysisService

app = FastAPI(title="Stock AI Worker")

@app.on_event("startup")
def startup_event():
    Config.validate()


@app.post("/analyze-stock", response_model=StockAnalysisResponse)
async def analyze_stock(payload: StockAnalysisRequest):
    try:
        service = FinancialAnalysisService()
        
        print(f"--> Recebida solicitação para analisar: {payload.symbol}")
        
        # Executa a IA (pode demorar 30-60s)
        result = await run_in_threadpool(service.execute_analysis, payload.symbol)
        
        print("<-- Análise concluída com sucesso.")

        return StockAnalysisResponse(
            message=result.get("report"), 
            dados=result.get("raw_data"),
            sentimento=result.get("raw_sentiment"),
            status="success"
        )

    except Exception as e:
        traceback.print_exc()
        error_msg = str(e).lower()
        
        if "429" in error_msg or "quota" in error_msg:
             raise HTTPException(status_code=429, detail={"message": "Cota da IA excedida. Tente em 1 minuto."})
        
        raise HTTPException(status_code=500, detail={"message": f"Erro interno: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
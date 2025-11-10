# --- models.py ---
from pydantic import BaseModel

class StockAnalysisRequest(BaseModel):
    """ O que a API espera receber no body """
    stock_symbol: str

class AnalysisResponse(BaseModel):
    """ O que a API promete devolver """
    message: str
    dados: str
    sentimento: str
    status: str
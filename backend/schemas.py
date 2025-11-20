from pydantic import BaseModel, Field
from typing import Optional

class StockAnalysisRequest(BaseModel):
   
    symbol: str = Field(..., min_length=2, max_length=10)

class StockAnalysisResponse(BaseModel):
    message: str
    dados: Optional[str]
    sentimento: Optional[str]
    status: str
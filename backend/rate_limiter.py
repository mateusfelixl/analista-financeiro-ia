# --- rate_limiter.py ---
import time
from fastapi import HTTPException

# Nossas variáveis de estado
last_request_time = 0
MIN_INTERVAL = 60 # Intervalo mínimo de 60 segundos

def check_rate_limit():
    """
    Esta função será "dependida" pelo endpoint.
    O FastAPI vai executá-la antes de rodar a nossa lógica.
    """
    global last_request_time
    
    time_since_last = time.time() - last_request_time
    
    if time_since_last < MIN_INTERVAL:
        wait_time = MIN_INTERVAL - time_since_last
        raise HTTPException(
            status_code=429,
            detail={
                "message": f"Rate limit atingido. Por favor, aguarde {wait_time:.0f} segundos.",
                "wait_seconds": int(wait_time)
            }
        )
    
    # Se passou, atualiza o tempo e permite a requisição continuar
    last_request_time = time.time()
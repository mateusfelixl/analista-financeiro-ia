import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    API_VERSION = "3.1.0"
    PROJECT_NAME = "Stock Insider AI Core"
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    GEMINI_MODEL = "gemini/gemini-2.5-flash"
    
    MIN_REQUEST_INTERVAL_SEC = 60

    @staticmethod
    def validate():
        if not Config.GOOGLE_API_KEY:
            raise ValueError("A configuração crítica GOOGLE_API_KEY não foi detectada.")
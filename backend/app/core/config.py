"""
Configuración de la aplicación
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Aplicación
    APP_NAME: str = "Sistema de Protección de Activos"
    VERSION: str = "1.0.0"
    
    # Base de datos
    DATABASE_URL: str
    
    # Seguridad
    SECRET_KEY: str = "tu-clave-secreta-super-segura-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 días
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

"""
FastAPI - Sistema de Protección de Activos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth

# Crear tablas
Base.metadata.create_all(bind=engine)

# Aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])

# Root endpoint
@app.get("/")
def read_root():
    return {
        "mensaje": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "✅ Operativo",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

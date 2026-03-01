"""
Sistema de Protección de Activos - API Principal
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import Base, engine
from app.routers import auth, cedis, scorecards, presupuestos, documentos

# Crear tablas
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Sistema de Protección de Activos",
    description="API para gestión de seguridad y protección civil",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(cedis.router, prefix="/api/cedis", tags=["CEDIS"])
app.include_router(scorecards.router, prefix="/api/scorecards", tags=["Scorecards"])
app.include_router(presupuestos.router, prefix="/api/presupuestos", tags=["Presupuestos"])
app.include_router(documentos.router, prefix="/api/documentos", tags=["Documentos"])

@app.get("/")
def root():
    return {
        "mensaje": "Sistema de Protección de Activos",
        "version": "1.0.0",
        "status": "✅ Operativo",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

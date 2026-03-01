"""
Modelo de CEDIS
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class CEDIS(Base):
    __tablename__ = "cedis"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False)
    estado = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    direccion = Column(String(500), nullable=True)
    responsable = Column(String(200), nullable=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(200), nullable=True)
    
    # Scores
    score_general = Column(Float, default=0.0)
    score_patrimonial = Column(Float, default=0.0)
    score_civil = Column(Float, default=0.0)
    score_sst = Column(Float, default=0.0)
    
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

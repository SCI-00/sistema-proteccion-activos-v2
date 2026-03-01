"""
Modelo de Scorecard
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Scorecard(Base):
    __tablename__ = "scorecards"
    
    id = Column(Integer, primary_key=True, index=True)
    cedis_id = Column(Integer, ForeignKey("cedis.id"), nullable=False)
    
    # Tipo de evaluación
    tipo_pilar = Column(String(50), nullable=False)  # patrimonial, civil, sst
    periodo = Column(String(20), nullable=False)  # 2026-02, 2026-03, etc
    
    # Scores detallados
    score_total = Column(Float, nullable=False)
    
    # Indicadores específicos
    indicador_1 = Column(String(200), nullable=True)
    valor_1 = Column(Float, nullable=True)
    
    indicador_2 = Column(String(200), nullable=True)
    valor_2 = Column(Float, nullable=True)
    
    indicador_3 = Column(String(200), nullable=True)
    valor_3 = Column(Float, nullable=True)
    
    indicador_4 = Column(String(200), nullable=True)
    valor_4 = Column(Float, nullable=True)
    
    indicador_5 = Column(String(200), nullable=True)
    valor_5 = Column(Float, nullable=True)
    
    # Observaciones
    observaciones = Column(Text, nullable=True)
    evaluador = Column(String(200), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

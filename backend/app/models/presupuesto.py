"""
Modelo de Presupuesto
"""
from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Presupuesto(Base):
    __tablename__ = "presupuestos"
    
    id = Column(Integer, primary_key=True, index=True)
    cedis_id = Column(Integer, ForeignKey("cedis.id"), nullable=False)
    
    # Información del gasto
    concepto = Column(String(300), nullable=False)
    categoria = Column(String(100), nullable=False)  # Nómina, Mantenimiento, Capacitación, etc
    monto = Column(Float, nullable=False)
    moneda = Column(String(10), default="MXN")
    
    # Fecha y período
    fecha_gasto = Column(Date, nullable=False)
    periodo = Column(String(20), nullable=False)  # 2026-02, 2026-03, etc
    
    # Detalles
    proveedor = Column(String(200), nullable=True)
    factura = Column(String(100), nullable=True)
    descripcion = Column(Text, nullable=True)
    
    # Control
    aprobado_por = Column(String(200), nullable=True)
    registrado_por = Column(String(200), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

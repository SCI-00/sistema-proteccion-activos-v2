"""
Modelo de Documento
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Documento(Base):
    __tablename__ = "documentos"
    
    id = Column(Integer, primary_key=True, index=True)
    cedis_id = Column(Integer, ForeignKey("cedis.id"), nullable=False)
    
    # Información del documento
    nombre = Column(String(300), nullable=False)
    tipo = Column(String(100), nullable=False)  # Análisis Riesgos, PIPC, Auditoría, etc
    categoria = Column(String(100), nullable=False)  # Patrimonial, Civil, SST
    
    # Archivo
    archivo_url = Column(String(500), nullable=False)  # URL o path del archivo
    archivo_nombre = Column(String(300), nullable=False)
    archivo_tipo = Column(String(50), nullable=False)  # pdf, docx, xlsx
    archivo_tamano = Column(Integer, nullable=True)  # en bytes
    
    # Metadata
    descripcion = Column(Text, nullable=True)
    fecha_documento = Column(DateTime(timezone=True), nullable=True)
    vigencia = Column(String(50), nullable=True)
    
    # Control
    subido_por = Column(String(200), nullable=True)
    version = Column(String(20), default="1.0")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

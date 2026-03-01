"""
Router de Documentos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.documento import Documento
from app.models.usuario import Usuario
from app.schemas import DocumentoCreate, DocumentoResponse

router = APIRouter()

@router.get("/", response_model=List[DocumentoResponse])
def get_all_documentos(
    skip: int = 0,
    limit: int = 100,
    cedis_id: int = None,
    tipo: str = None,
    categoria: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener documentos con filtros opcionales"""
    query = db.query(Documento)
    
    if cedis_id:
        query = query.filter(Documento.cedis_id == cedis_id)
    if tipo:
        query = query.filter(Documento.tipo == tipo)
    if categoria:
        query = query.filter(Documento.categoria == categoria)
    
    documentos = query.offset(skip).limit(limit).all()
    return documentos

@router.get("/{documento_id}", response_model=DocumentoResponse)
def get_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener un documento por ID"""
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento

@router.post("/", response_model=DocumentoResponse, status_code=status.HTTP_201_CREATED)
def create_documento(
    documento_data: DocumentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nuevo documento"""
    db_documento = Documento(**documento_data.model_dump())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

@router.delete("/{documento_id}")
def delete_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar documento"""
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    db.delete(documento)
    db.commit()
    return {"message": "Documento eliminado exitosamente"}

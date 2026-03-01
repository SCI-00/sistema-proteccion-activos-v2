"""
Router de CEDIS
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.cedis import CEDIS
from app.models.usuario import Usuario
from app.schemas import CEDISCreate, CEDISUpdate, CEDISResponse

router = APIRouter()

@router.get("/", response_model=List[CEDISResponse])
def get_all_cedis(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener todos los CEDIS"""
    cedis = db.query(CEDIS).offset(skip).limit(limit).all()
    return cedis

@router.get("/{cedis_id}", response_model=CEDISResponse)
def get_cedis(
    cedis_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener un CEDIS por ID"""
    cedis = db.query(CEDIS).filter(CEDIS.id == cedis_id).first()
    if not cedis:
        raise HTTPException(status_code=404, detail="CEDIS no encontrado")
    return cedis

@router.post("/", response_model=CEDISResponse, status_code=status.HTTP_201_CREATED)
def create_cedis(
    cedis_data: CEDISCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nuevo CEDIS"""
    # Verificar si el código ya existe
    existing = db.query(CEDIS).filter(CEDIS.codigo == cedis_data.codigo).first()
    if existing:
        raise HTTPException(status_code=400, detail="Código de CEDIS ya existe")
    
    db_cedis = CEDIS(**cedis_data.model_dump())
    db.add(db_cedis)
    db.commit()
    db.refresh(db_cedis)
    return db_cedis

@router.put("/{cedis_id}", response_model=CEDISResponse)
def update_cedis(
    cedis_id: int,
    cedis_data: CEDISUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar CEDIS"""
    cedis = db.query(CEDIS).filter(CEDIS.id == cedis_id).first()
    if not cedis:
        raise HTTPException(status_code=404, detail="CEDIS no encontrado")
    
    for key, value in cedis_data.model_dump(exclude_unset=True).items():
        setattr(cedis, key, value)
    
    db.commit()
    db.refresh(cedis)
    return cedis

@router.delete("/{cedis_id}")
def delete_cedis(
    cedis_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar CEDIS"""
    cedis = db.query(CEDIS).filter(CEDIS.id == cedis_id).first()
    if not cedis:
        raise HTTPException(status_code=404, detail="CEDIS no encontrado")
    
    db.delete(cedis)
    db.commit()
    return {"message": "CEDIS eliminado exitosamente"}

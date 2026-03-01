"""
Router de Presupuestos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.presupuesto import Presupuesto
from app.models.usuario import Usuario
from app.schemas import PresupuestoCreate, PresupuestoResponse

router = APIRouter()

@router.get("/", response_model=List[PresupuestoResponse])
def get_all_presupuestos(
    skip: int = 0,
    limit: int = 100,
    cedis_id: int = None,
    categoria: str = None,
    periodo: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener presupuestos con filtros opcionales"""
    query = db.query(Presupuesto)
    
    if cedis_id:
        query = query.filter(Presupuesto.cedis_id == cedis_id)
    if categoria:
        query = query.filter(Presupuesto.categoria == categoria)
    if periodo:
        query = query.filter(Presupuesto.periodo == periodo)
    
    presupuestos = query.offset(skip).limit(limit).all()
    return presupuestos

@router.get("/{presupuesto_id}", response_model=PresupuestoResponse)
def get_presupuesto(
    presupuesto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener un presupuesto por ID"""
    presupuesto = db.query(Presupuesto).filter(Presupuesto.id == presupuesto_id).first()
    if not presupuesto:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return presupuesto

@router.post("/", response_model=PresupuestoResponse, status_code=status.HTTP_201_CREATED)
def create_presupuesto(
    presupuesto_data: PresupuestoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nuevo presupuesto"""
    db_presupuesto = Presupuesto(**presupuesto_data.model_dump())
    db.add(db_presupuesto)
    db.commit()
    db.refresh(db_presupuesto)
    return db_presupuesto

@router.delete("/{presupuesto_id}")
def delete_presupuesto(
    presupuesto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar presupuesto"""
    presupuesto = db.query(Presupuesto).filter(Presupuesto.id == presupuesto_id).first()
    if not presupuesto:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    
    db.delete(presupuesto)
    db.commit()
    return {"message": "Presupuesto eliminado exitosamente"}

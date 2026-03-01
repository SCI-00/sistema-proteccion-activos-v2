"""
Router de Scorecards
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.scorecard import Scorecard
from app.models.usuario import Usuario
from app.schemas import ScorecardCreate, ScorecardResponse

router = APIRouter()

@router.get("/", response_model=List[ScorecardResponse])
def get_all_scorecards(
    skip: int = 0,
    limit: int = 100,
    cedis_id: int = None,
    tipo_pilar: str = None,
    periodo: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener scorecards con filtros opcionales"""
    query = db.query(Scorecard)
    
    if cedis_id:
        query = query.filter(Scorecard.cedis_id == cedis_id)
    if tipo_pilar:
        query = query.filter(Scorecard.tipo_pilar == tipo_pilar)
    if periodo:
        query = query.filter(Scorecard.periodo == periodo)
    
    scorecards = query.offset(skip).limit(limit).all()
    return scorecards

@router.get("/{scorecard_id}", response_model=ScorecardResponse)
def get_scorecard(
    scorecard_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener un scorecard por ID"""
    scorecard = db.query(Scorecard).filter(Scorecard.id == scorecard_id).first()
    if not scorecard:
        raise HTTPException(status_code=404, detail="Scorecard no encontrado")
    return scorecard

@router.post("/", response_model=ScorecardResponse, status_code=status.HTTP_201_CREATED)
def create_scorecard(
    scorecard_data: ScorecardCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear nuevo scorecard"""
    db_scorecard = Scorecard(**scorecard_data.model_dump())
    db.add(db_scorecard)
    db.commit()
    db.refresh(db_scorecard)
    return db_scorecard

@router.delete("/{scorecard_id}")
def delete_scorecard(
    scorecard_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar scorecard"""
    scorecard = db.query(Scorecard).filter(Scorecard.id == scorecard_id).first()
    if not scorecard:
        raise HTTPException(status_code=404, detail="Scorecard no encontrado")
    
    db.delete(scorecard)
    db.commit()
    return {"message": "Scorecard eliminado exitosamente"}

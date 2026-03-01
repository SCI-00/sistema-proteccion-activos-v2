"""
Schemas de Pydantic
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

# ========== USUARIOS ==========
class UserBase(BaseModel):
    email: EmailStr
    nombre: str

class UserCreate(UserBase):
    password: str
    rol: str = "Usuario"
    organizacion_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    rol: str
    activo: bool
    organizacion_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None

# ========== CEDIS ==========
class CEDISBase(BaseModel):
    nombre: str
    codigo: str
    estado: str
    ciudad: str
    direccion: Optional[str] = None
    responsable: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

class CEDISCreate(CEDISBase):
    pass

class CEDISUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    estado: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    responsable: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    score_general: Optional[float] = None
    score_patrimonial: Optional[float] = None
    score_civil: Optional[float] = None
    score_sst: Optional[float] = None
    activo: Optional[bool] = None

class CEDISResponse(CEDISBase):
    id: int
    score_general: float
    score_patrimonial: float
    score_civil: float
    score_sst: float
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== SCORECARDS ==========
class ScorecardBase(BaseModel):
    cedis_id: int
    tipo_pilar: str
    periodo: str
    score_total: float
    indicador_1: Optional[str] = None
    valor_1: Optional[float] = None
    indicador_2: Optional[str] = None
    valor_2: Optional[float] = None
    indicador_3: Optional[str] = None
    valor_3: Optional[float] = None
    indicador_4: Optional[str] = None
    valor_4: Optional[float] = None
    indicador_5: Optional[str] = None
    valor_5: Optional[float] = None
    observaciones: Optional[str] = None
    evaluador: Optional[str] = None

class ScorecardCreate(ScorecardBase):
    pass

class ScorecardResponse(ScorecardBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== PRESUPUESTOS ==========
class PresupuestoBase(BaseModel):
    cedis_id: int
    concepto: str
    categoria: str
    monto: float
    moneda: str = "MXN"
    fecha_gasto: date
    periodo: str
    proveedor: Optional[str] = None
    factura: Optional[str] = None
    descripcion: Optional[str] = None
    aprobado_por: Optional[str] = None
    registrado_por: Optional[str] = None

class PresupuestoCreate(PresupuestoBase):
    pass

class PresupuestoResponse(PresupuestoBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== DOCUMENTOS ==========
class DocumentoBase(BaseModel):
    cedis_id: int
    nombre: str
    tipo: str
    categoria: str
    archivo_url: str
    archivo_nombre: str
    archivo_tipo: str
    archivo_tamano: Optional[int] = None
    descripcion: Optional[str] = None
    fecha_documento: Optional[datetime] = None
    vigencia: Optional[str] = None
    subido_por: Optional[str] = None
    version: str = "1.0"

class DocumentoCreate(DocumentoBase):
    pass

class DocumentoResponse(DocumentoBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

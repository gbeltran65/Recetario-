from typing import List
from pydantic import BaseModel

class RecetaCreate(BaseModel):
    id: int
    nombre: str
    tiempo_preparacion: int
    porciones: int
    categoria: str
    ingredientes: List[str]
    instrucciones: str
    estado: str

class RecetaOut(RecetaCreate):
    class Config:
        orm_mode = True

class IngredienteCreate(BaseModel):
    id: int
    nombre: str
    unidad: str
    cantidad: float
    estado: str

class IngredienteOut(IngredienteCreate):
    class Config:
        orm_mode = True

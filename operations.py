from sqlalchemy.orm import Session
from models import Receta, Ingrediente
from typing import List, Optional
from fastapi import HTTPException

# ================== RECETAS ==================

def crear_receta(db: Session, receta: Receta) -> Receta:
    db.add(receta)
    db.commit()
    db.refresh(receta)
    return receta

def obtener_recetas_activas(db: Session) -> List[Receta]:
    return db.query(Receta).filter(Receta.estado == "activo").all()

def buscar_receta_por_id(db: Session, id: int) -> Optional[Receta]:
    return db.query(Receta).filter(Receta.id == id).first()

def actualizar_receta(db: Session, id: int, nueva: Receta) -> Receta:
    receta = buscar_receta_por_id(db, id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada.")
    for attr, value in nueva.__dict__.items():
        setattr(receta, attr, value)
    db.commit()
    db.refresh(receta)
    return receta

def eliminar_receta(db: Session, id: int):
    receta = buscar_receta_por_id(db, id)
    if receta:
        receta.estado = "eliminado"
        db.commit()
        return {"mensaje": "Receta eliminada."}
    raise HTTPException(status_code=404, detail="Receta no encontrada.")

def filtrar_recetas_por_categoria(db: Session, categoria: str) -> List[Receta]:
    return db.query(Receta).filter(Receta.estado == "activo", Receta.categoria.ilike(categoria)).all()

def buscar_recetas_por_nombre(db: Session, nombre: str) -> List[Receta]:
    return db.query(Receta).filter(Receta.estado == "activo", Receta.nombre.ilike(f"%{nombre}%")).all()

# ================== INGREDIENTES ==================

def crear_ingrediente(db: Session, ingrediente: Ingrediente) -> Ingrediente:
    db.add(ingrediente)
    db.commit()
    db.refresh(ingrediente)
    return ingrediente

def obtener_ingredientes_activos(db: Session) -> List[Ingrediente]:
    return db.query(Ingrediente).filter(Ingrediente.estado == "activo").all()

def buscar_ingrediente_por_id(db: Session, id: int) -> Optional[Ingrediente]:
    return db.query(Ingrediente).filter(Ingrediente.id == id).first()

def actualizar_ingrediente(db: Session, id: int, nuevo: Ingrediente) -> Ingrediente:
    ingrediente = buscar_ingrediente_por_id(db, id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado.")
    for attr, value in nuevo.__dict__.items():
        setattr(ingrediente, attr, value)
    db.commit()
    db.refresh(ingrediente)
    return ingrediente

def eliminar_ingrediente(db: Session, id: int):
    ingrediente = buscar_ingrediente_por_id(db, id)
    if ingrediente:
        ingrediente.estado = "eliminado"
        db.commit()
        return {"mensaje": "Ingrediente eliminado."}
    raise HTTPException(status_code=404, detail="Ingrediente no encontrado.")

def filtrar_ingredientes_por_unidad(db: Session, unidad: str) -> List[Ingrediente]:
    return db.query(Ingrediente).filter(Ingrediente.estado == "activo", Ingrediente.unidad.ilike(unidad)).all()

def buscar_ingredientes_por_nombre(db: Session, nombre: str) -> List[Ingrediente]:
    return db.query(Ingrediente).filter(Ingrediente.estado == "activo", Ingrediente.nombre.ilike(f"%{nombre}%")).all()

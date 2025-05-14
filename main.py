from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Receta, Ingrediente
import operations as op
from schemas import RecetaCreate, RecetaOut, IngredienteCreate, IngredienteOut
from typing import List

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== ENDPOINTS RECETAS ====================

@app.post("/recetas", response_model=RecetaOut)
def crear_receta(receta: RecetaCreate, db: Session = Depends(get_db)):
    if op.buscar_receta_por_id(db, receta.id):
        raise HTTPException(status_code=400, detail="Ya existe una receta con ese ID.")
    nueva_receta = Receta(**receta.dict())  # conversión Pydantic → SQLAlchemy
    return op.crear_receta(db, nueva_receta)

@app.get("/recetas", response_model=List[RecetaOut])
def obtener_recetas(db: Session = Depends(get_db)):
    return op.obtener_recetas_activas(db)

@app.get("/recetas/{receta_id}", response_model=RecetaOut)
def obtener_receta_por_id(receta_id: int, db: Session = Depends(get_db)):
    receta = op.buscar_receta_por_id(db, receta_id)
    if not receta or receta.estado != "activo":
        raise HTTPException(status_code=404, detail="Receta no encontrada.")
    return receta

@app.put("/recetas/{receta_id}", response_model=RecetaOut)
def actualizar_receta(receta_id: int, nueva: RecetaCreate, db: Session = Depends(get_db)):
    receta_existente = op.buscar_receta_por_id(db, receta_id)
    if not receta_existente:
        raise HTTPException(status_code=404, detail="Receta no encontrada.")
    nueva_receta = Receta(**nueva.dict())
    return op.actualizar_receta(db, receta_id, nueva_receta)

@app.delete("/recetas/{receta_id}")
def eliminar_receta(receta_id: int, db: Session = Depends(get_db)):
    receta = op.buscar_receta_por_id(db, receta_id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada.")
    return op.eliminar_receta(db, receta_id)

@app.get("/recetas/categoria/{categoria}", response_model=List[RecetaOut])
def filtrar_recetas_por_categoria(categoria: str, db: Session = Depends(get_db)):
    return op.filtrar_recetas_por_categoria(db, categoria)

@app.get("/recetas/buscar/{nombre}", response_model=List[RecetaOut])
def buscar_recetas_por_nombre(nombre: str, db: Session = Depends(get_db)):
    return op.buscar_recetas_por_nombre(db, nombre)

# ==================== ENDPOINTS INGREDIENTES ====================

@app.post("/ingredientes", response_model=IngredienteOut)
def crear_ingrediente(ingrediente: IngredienteCreate, db: Session = Depends(get_db)):
    if op.buscar_ingrediente_por_id(db, ingrediente.id):
        raise HTTPException(status_code=400, detail="Ya existe un ingrediente con ese ID.")
    nuevo = Ingrediente(**ingrediente.dict())
    return op.crear_ingrediente(db, nuevo)

@app.get("/ingredientes", response_model=List[IngredienteOut])
def obtener_ingredientes(db: Session = Depends(get_db)):
    return op.obtener_ingredientes_activos(db)

@app.get("/ingredientes/{ingrediente_id}", response_model=IngredienteOut)
def obtener_ingrediente_por_id(ingrediente_id: int, db: Session = Depends(get_db)):
    ingrediente = op.buscar_ingrediente_por_id(db, ingrediente_id)
    if not ingrediente or ingrediente.estado != "activo":
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado.")
    return ingrediente

@app.put("/ingredientes/{ingrediente_id}", response_model=IngredienteOut)
def actualizar_ingrediente(ingrediente_id: int, nuevo: IngredienteCreate, db: Session = Depends(get_db)):
    if not op.buscar_ingrediente_por_id(db, ingrediente_id):
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado.")
    nuevo_ingrediente = Ingrediente(**nuevo.dict())
    return op.actualizar_ingrediente(db, ingrediente_id, nuevo_ingrediente)

@app.delete("/ingredientes/{ingrediente_id}")
def eliminar_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    ingrediente = op.buscar_ingrediente_por_id(db, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado.")
    return op.eliminar_ingrediente(db, ingrediente_id)

@app.get("/ingredientes/unidad/{unidad}", response_model=List[IngredienteOut])
def filtrar_ingredientes_por_unidad(unidad: str, db: Session = Depends(get_db)):
    return op.filtrar_ingredientes_por_unidad(db, unidad)

@app.get("/ingredientes/buscar/{nombre}", response_model=List[IngredienteOut])
def buscar_ingredientes_por_nombre(nombre: str, db: Session = Depends(get_db)):
    return op.buscar_ingredientes_por_nombre(db, nombre)

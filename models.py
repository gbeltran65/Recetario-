from sqlalchemy import Column, Integer, String, Float, Text, ARRAY
from database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tiempo_preparacion = Column(Integer)
    porciones = Column(Integer)
    categoria = Column(String)
    ingredientes = Column(ARRAY(String))  # o Text para guardar JSON
    instrucciones = Column(Text)
    estado = Column(String, default="activo")


class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    unidad = Column(String)
    cantidad = Column(Float)
    estado = Column(String, default="activo")

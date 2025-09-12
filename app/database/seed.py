from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.session import SessionLocal
from app.database.entities import Brand, Locality

DEFAULT_BRANDS = [
    "Toyota", "Mazda", "Chevrolet", "Renault", "Nissan",
]
DEFAULT_LOCALITIES = [
    "Usaquen", "Chapinero", "Santa Fe", "San Cristobal", "Usme",
    "Tunjuelito", "Bosa", "Kennedy", "Fontibon", "Engativa",
    "Suba", "Barrios Unidos", "Teusaquillo", "Los Martires",
    "Antonio Nariño", "Puente Aranda", "La Candelaria", "Rafael Uribe Uribe",
    "Ciudad Bolivar", "Sumapaz",
]

def upsert_brand(session: Session, name: str):
    exists = session.scalar(select(Brand).where(Brand.name == name))
    if not exists:
        session.add(Brand(name=name))
        return True
    return False

def upsert_locality(session: Session, name: str):
    exists = session.scalar(select(Locality).where(Locality.name == name))
    if not exists:
        session.add(Locality(name=name))
        return True
    return False

def run():
    inserted = {"brands": 0, "localities": 0}
    with SessionLocal() as session:
        for b in DEFAULT_BRANDS:
            if upsert_brand(session, b):
                inserted["brands"] += 1
        for l in DEFAULT_LOCALITIES:
            if upsert_locality(session, l):
                inserted["localities"] += 1
        session.commit()
    print(f"Seed: {inserted}")

if __name__ == "__main__":
    run()

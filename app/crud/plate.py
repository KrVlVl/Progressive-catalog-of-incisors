from sqlalchemy.orm import Session
from app import models
from app.schemas import PlateCreate, PlateUpdate

def get_plate(db: Session, plate_id: int):
    return db.query(models.CuttingPlate).filter(models.CuttingPlate.id == plate_id).first()

def get_plates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CuttingPlate).offset(skip).limit(limit).all()

def create_plate(db: Session, plate: PlateCreate):
    db_plate = models.CuttingPlate(**plate.model_dump())
    db.add(db_plate)
    db.commit()
    db.refresh(db_plate)
    return db_plate

def update_plate(db: Session, plate_id: int, plate_update: PlateUpdate):
    db_plate = get_plate(db, plate_id)
    if not db_plate:
        return None
    
    update_data = plate_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plate, field, value)
    
    db.commit()
    db.refresh(db_plate)
    return db_plate

def delete_plate(db: Session, plate_id: int):
    db_plate = get_plate(db, plate_id)
    if db_plate:
        db.delete(db_plate)
        db.commit()
        return True
    return False
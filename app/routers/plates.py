from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, auth, models
from app.crud import plate as plate_crud
from app.database import get_db

router = APIRouter(prefix="/plates", tags=["Управление пластинами"])

def enrich_plate_with_category(db: Session, plate):
    """Добавляет категорию к пластине"""
    if plate and plate.category_id:
        plate.category = db.query(models.PlateCategory).filter(models.PlateCategory.id == plate.category_id).first()
    return plate

@router.post("/", response_model=schemas.PlateOut, status_code=status.HTTP_201_CREATED, 
             summary="Создать пластину", description="Добавление новой режущей пластины в базу данных")
def create_plate(
    plate: schemas.PlateCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Создание новой режущей пластины (требуется авторизация)"""
    db_plate = plate_crud.create_plate(db=db, plate=plate)
    db_plate = enrich_plate_with_category(db, db_plate)
    return db_plate

@router.get("/", response_model=List[schemas.PlateOut], 
            summary="Получить список пластин", description="Возвращает список всех режущих пластин")
def read_plates(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Получение списка всех пластин с пагинацией (требуется авторизация)"""
    plates = plate_crud.get_plates(db, skip=skip, limit=limit)
    for plate in plates:
        enrich_plate_with_category(db, plate)
    return plates

@router.get("/{plate_id}", response_model=schemas.PlateOut, 
            summary="Получить пластину по ID", description="Возвращает информацию о конкретной пластине")
def read_plate(
    plate_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Получение пластины по её идентификатору (требуется авторизация)"""
    db_plate = plate_crud.get_plate(db, plate_id=plate_id)
    if db_plate is None:
        raise HTTPException(status_code=404, detail="Пластина не найдена")
    db_plate = enrich_plate_with_category(db, db_plate)
    return db_plate

@router.put("/{plate_id}", response_model=schemas.PlateOut, 
            summary="Обновить пластину", description="Обновление информации о режущей пластине")
def update_plate(
    plate_id: int,
    plate_update: schemas.PlateUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Обновление данных пластины (требуется авторизация)"""
    db_plate = plate_crud.update_plate(db, plate_id, plate_update)
    if db_plate is None:
        raise HTTPException(status_code=404, detail="Пластина не найдена")
    db_plate = enrich_plate_with_category(db, db_plate)
    return db_plate

@router.delete("/{plate_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить пластину", description="Удаление режущей пластины из базы данных")
def delete_plate(
    plate_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Удаление пластины (требуется авторизация)"""
    success = plate_crud.delete_plate(db, plate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пластина не найдена")
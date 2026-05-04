from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, auth, models
from app.database import get_db
from app.algorithms import matcher

router = APIRouter(prefix="/select", tags=["Подбор пластин"])

@router.post("/plate", response_model=schemas.SelectionResponse, 
             summary="Подобрать пластину", 
             description="Алгоритмический подбор оптимальной режущей пластины на основе параметров обработки")
def select_plate(
    request: schemas.SelectionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """
    Подбор оптимальной режущей пластины
    
    Алгоритм учитывает:
    - Группу обрабатываемого материала
    - Глубину резания
    - Тип обработки (черновая/чистовая)
    - Бюджет (опционально)
    
    Возвращает топ-5 наиболее подходящих пластин с рейтингом совместимости
    """
    # Получаем все пластины из БД
    all_plates = db.query(models.CuttingPlate).all()
    
    if not all_plates:
        raise HTTPException(status_code=404, detail="В базе данных нет пластин")
    
    # Загружаем категории для всех пластин
    for plate in all_plates:
        if plate.category_id:
            plate.category = db.query(models.PlateCategory).filter(models.PlateCategory.id == plate.category_id).first()
    
    # Вызываем алгоритм подбора
    recommendations = matcher.match_plates(
        plates=all_plates,
        material_group=request.material_group,
        cutting_depth=request.cutting_depth_mm,
        operation_type=request.operation_type,
        max_price=request.max_price
    )
    
    # Формируем ответ
    plate_recommendations = []
    for plate, score, reason in recommendations:
        plate_out = schemas.PlateOut.model_validate(plate)
        plate_recommendations.append(
            schemas.PlateRecommendation(
                plate=plate_out,
                match_score=score,
                reason=reason
            )
        )
    
    return schemas.SelectionResponse(
        recommendations=plate_recommendations,
        total_found=len(plate_recommendations),
        algorithm_version="v1.0"
    )
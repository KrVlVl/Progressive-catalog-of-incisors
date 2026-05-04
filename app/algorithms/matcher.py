from typing import List, Tuple, Optional
from app import models


def match_plates(
    plates: List[models.CuttingPlate],
    material_group: str,
    cutting_depth: float,
    operation_type: str,
    max_price: Optional[float] = None
) -> List[Tuple[models.CuttingPlate, float, str]]:
    
    results = []

    for plate in plates:
        score = 0
        reasons = []

        # Критерий 1: Группа материала (вес 30%)
        score, reasons = _evaluate_material_group(
            plate, material_group, score, reasons
        )

        # Критерий 2: Глубина резания (вес 25%)
        score, reasons = _evaluate_cutting_depth(
            plate, cutting_depth, score, reasons
        )

        # Критерий 3: Тип обработки (вес 20%)
        score, reasons = _evaluate_operation_type(
            plate, operation_type, score, reasons
        )

        # Критерий 4: Материал и покрытие (вес 15%)
        score, reasons = _evaluate_material_and_coating(plate, score, reasons)

        # Критерий 5: Цена (штраф)
        if max_price and plate.price > max_price:
            score, reasons = _apply_price_penalty(plate, max_price, score, reasons)

        if score > 0:
            results.append((plate, round(score, 1), "; ".join(reasons)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]


def _evaluate_material_group(plate, material_group, score, reasons):
    plate_group = plate.material_group.upper()
    target_group = material_group.upper()

    if plate_group == target_group:
        score += 30
        reasons.append("✓ Полностью подходит для данной группы материала")
    elif target_group in plate_group:
        score += 15
        reasons.append("⚠ Частично подходит для группы материала")
    else:
        reasons.append("✗ Не рекомендована для данной группы материала")
    return score, reasons


def _evaluate_cutting_depth(plate, cutting_depth, score, reasons):
    """Оценивает соответствие глубины резания."""
    if cutting_depth <= plate.max_depth_mm:
        score += 25
        reasons.append(
            f"✓ Глубина резания в пределах нормы (макс. {plate.max_depth_mm} мм)"
        )
    else:
        penalty = min(25, int((cutting_depth - plate.max_depth_mm) /
                       plate.max_depth_mm * 25))
        score += max(0, 25 - penalty)
        reasons.append(
            f"⚠ Превышение макс. глубины на {cutting_depth - plate.max_depth_mm:.1f} мм"
        )
    return score, reasons


def _evaluate_operation_type(plate, operation_type, score, reasons):
    """Оценивает соответствие типу обработки."""
    op_type = operation_type.lower()

    if op_type == "черновая":
        if "heavy" in plate.name.lower() or "rough" in plate.name.lower():
            score += 20
            reasons.append("✓ Оптимальна для черновой обработки")
        else:
            score += 10
            reasons.append("⚠ Может использоваться для черновой обработки")
    elif op_type == "чистовая":
        if "finish" in plate.name.lower() or "precision" in plate.name.lower():
            score += 20
            reasons.append("✓ Оптимальна для чистовой обработки")
        else:
            score += 10
            reasons.append("⚠ Может использоваться для чистовой обработки")
    return score, reasons


def _evaluate_material_and_coating(plate, score, reasons):
    """Оценивает материал и покрытие пластины."""
    material_scores = {
        "Карбид": (10, "✓ Карбид - универсальный материал"),
        "Керамика": (8, "✓ Керамика для высоких скоростей"),
        "CBN": (12, "✓ CBN для закаленных сталей")
    }

    material_score = 0
    if plate.material in material_scores:
        material_score, reason_text = material_scores[plate.material]
        reasons.append(reason_text)

    coating_bonus = {
        "TiAlN": 5,
        "AlTiN": 5,
        "TiN": 3
    }

    if plate.coating in coating_bonus:
        material_score += coating_bonus[plate.coating]
        if plate.coating in ["TiAlN", "AlTiN"]:
            reasons.append("✓ Покрытие TiAlN/AlTiN повышает стойкость")
        elif plate.coating == "TiN":
            reasons.append("✓ Покрытие TiN для универсальных задач")

    score += min(15, material_score)
    return score, reasons


def _apply_price_penalty(plate, max_price, score, reasons):
    """Применяет штраф за превышение максимальной цены."""
    penalty = min(20, int((plate.price - max_price) / max_price * 20))
    score = max(0, score - penalty)
    reasons.append(f"⚠ Превышение бюджета на {plate.price - max_price:.0f} руб.")
    return score, reasons
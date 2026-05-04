from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

# Схемы для пользователей
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: str = Field(..., description="Email адрес")
    password: str = Field(..., min_length=6, description="Пароль (минимум 6 символов)")

class UserOut(BaseModel):
    id: int = Field(..., description="ID пользователя")
    username: str = Field(..., description="Имя пользователя")
    email: str = Field(..., description="Email адрес")
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field(default="bearer", description="Тип токена")

class TokenData(BaseModel):
    username: Optional[str] = None

# Схемы для категорий
class CategoryCreate(BaseModel):
    name: str = Field(..., description="Название категории")
    description: str = Field(..., description="Описание категории")
    hardness_range: str = Field(..., description="Диапазон твердости")

class CategoryOut(BaseModel):
    id: int = Field(..., description="ID категории")
    name: str = Field(..., description="Название категории")
    description: str = Field(..., description="Описание категории")
    hardness_range: str = Field(..., description="Диапазон твердости")
    
    model_config = ConfigDict(from_attributes=True)

# Схемы для пластин
class PlateCreate(BaseModel):
    name: str = Field(..., description="Название/модель пластины")
    material: str = Field(..., description="Материал пластины (Карбид, Керамика, CBN)")
    coating: Optional[str] = Field(None, description="Покрытие (TiN, TiAlN, AlTiN)")
    price: float = Field(..., gt=0, description="Цена в рублях")
    stock_quantity: int = Field(0, ge=0, description="Количество на складе")
    material_group: str = Field(..., description="Группа материала (P, M, K, N, S, H)")
    max_depth_mm: float = Field(..., gt=0, description="Максимальная глубина резания (мм)")
    recommended_speed_m_min: int = Field(..., description="Рекомендуемая скорость резания (м/мин)")
    category_id: int = Field(..., description="ID категории пластины")

class PlateUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название/модель пластины")
    price: Optional[float] = Field(None, gt=0, description="Цена в рублях")
    stock_quantity: Optional[int] = Field(None, ge=0, description="Количество на складе")
    max_depth_mm: Optional[float] = Field(None, gt=0, description="Максимальная глубина резания (мм)")

class PlateOut(BaseModel):
    id: int = Field(..., description="ID пластины")
    name: str = Field(..., description="Название/модель пластины")
    material: str = Field(..., description="Материал пластины")
    coating: Optional[str] = Field(None, description="Покрытие")
    price: float = Field(..., description="Цена в рублях")
    stock_quantity: int = Field(..., description="Количество на складе")
    material_group: str = Field(..., description="Группа материала")
    max_depth_mm: float = Field(..., description="Максимальная глубина резания (мм)")
    recommended_speed_m_min: int = Field(..., description="Рекомендуемая скорость резания (м/мин)")
    category_id: int = Field(..., description="ID категории")
    category: Optional[CategoryOut] = Field(None, description="Категория пластины")
    
    model_config = ConfigDict(from_attributes=True)

# Схемы для бизнес-задачи
class SelectionRequest(BaseModel):
    material_group: str = Field(..., description="Группа материала: P (сталь), M (нержавейка), K (чугун), N (алюминий), S (титан), H (закаленная сталь)")
    cutting_depth_mm: float = Field(..., gt=0, le=20, description="Глубина резания в миллиметрах")
    operation_type: str = Field(..., description="Тип обработки: черновая или чистовая")
    max_price: Optional[float] = Field(None, gt=0, description="Максимальная цена в рублях (опционально)")

class PlateRecommendation(BaseModel):
    plate: PlateOut = Field(..., description="Рекомендуемая пластина")
    match_score: float = Field(..., ge=0, le=100, description="Процент совместимости (0-100)")
    reason: str = Field(..., description="Причина выбора")

class SelectionResponse(BaseModel):
    recommendations: List[PlateRecommendation] = Field(..., description="Список рекомендаций")
    total_found: int = Field(..., description="Всего найдено подходящих пластин")
    algorithm_version: str = Field(..., description="Версия алгоритма подбора")
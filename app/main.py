from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import engine, Base, get_db
from app import models, auth as auth_module
from app.schemas import UserCreate, PlateCreate
from app.algorithms.matcher import match_plates
from app.crud import user as user_crud
from app.crud import plate as plate_crud
from app.routers import auth, plates, selection, styles

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Сервис подбора режущих пластин", version="1.0.0")

# Подключаем API роутеры (для тестов и API запросов)
app.include_router(auth.router)
app.include_router(plates.router)
app.include_router(selection.router)
app.include_router(styles.router)

# Настройка шаблонов
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Вспомогательная функция для получения пользователя из cookie
async def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        from jose import jwt
        from app.auth import SECRET_KEY, ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username:
            user = db.query(models.User).filter(models.User.username == username).first()
            return user
    except:
        return None
    return None

# ============= ВЕБ-СТРАНИЦЫ (HTML) =============

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_from_cookie(request, db)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

# Регистрация
@app.get("/web/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/web/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Проверка существования пользователя
    existing = db.query(models.User).filter(
        (models.User.username == username) | (models.User.email == email)
    ).first()
    
    if existing:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пользователь с таким именем или email уже существует"}
        )
    
    # Создание пользователя
    user_data = UserCreate(username=username, email=email, password=password)
    user_crud.create_user(db=db, user=user_data)
    
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "message": "Регистрация успешна! Теперь войдите в систему"}
    )

# Вход в систему
@app.get("/web/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/web/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = auth_module.authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Неверное имя пользователя или пароль"}
        )
    
    from datetime import timedelta
    token = auth_module.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    
    response = RedirectResponse(url="/web/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

# Выход
@app.get("/web/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

# Панель управления (список пластин)
@app.get("/web/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/web/login", status_code=303)
    
    plates_list = db.query(models.CuttingPlate).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "plates": plates_list}
    )

# Добавление пластины
@app.post("/web/add-plate", response_class=HTMLResponse)
async def add_plate(
    request: Request,
    name: str = Form(...),
    material: str = Form(...),
    coating: str = Form(None),
    price: float = Form(...),
    stock_quantity: int = Form(...),
    material_group: str = Form(...),
    max_depth_mm: float = Form(...),
    recommended_speed_m_min: int = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/web/login", status_code=303)
    
    plate_data = PlateCreate(
        name=name, 
        material=material, 
        coating=coating if coating else None,
        price=price, 
        stock_quantity=stock_quantity, 
        material_group=material_group,
        max_depth_mm=max_depth_mm, 
        recommended_speed_m_min=recommended_speed_m_min,
        category_id=category_id
    )
    plate_crud.create_plate(db=db, plate=plate_data)
    
    return RedirectResponse(url="/web/dashboard", status_code=303)

# Удаление пластины
@app.get("/web/delete-plate/{plate_id}")
async def delete_plate(plate_id: int, request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/web/login", status_code=303)
    
    plate_crud.delete_plate(db, plate_id)
    return RedirectResponse(url="/web/dashboard", status_code=303)

# Страница подбора пластины
@app.get("/web/select-page", response_class=HTMLResponse)
async def select_page(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/web/login", status_code=303)
    
    return templates.TemplateResponse(
        "select.html", 
        {
            "request": request, 
            "user": user,
            "recommendations": None,
            "selected_group": "P",
            "selected_depth": 3.0,
            "selected_operation": "черновая",
            "selected_price": None
        }
    )

# Обработка подбора пластины
@app.post("/web/select-plate", response_class=HTMLResponse)
async def select_plate_web(
    request: Request,
    material_group: str = Form(...),
    cutting_depth_mm: float = Form(...),
    operation_type: str = Form(...),
    max_price: float = Form(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/web/login", status_code=303)
    
    # Получаем все пластины
    all_plates = db.query(models.CuttingPlate).all()
    
    # Вызываем алгоритм подбора
    recommendations = match_plates(
        plates=all_plates,
        material_group=material_group,
        cutting_depth=cutting_depth_mm,
        operation_type=operation_type,
        max_price=max_price if max_price and max_price > 0 else None
    )
    
    return templates.TemplateResponse(
        "select.html",
        {
            "request": request,
            "user": user,
            "recommendations": recommendations,
            "selected_group": material_group,
            "selected_depth": cutting_depth_mm,
            "selected_operation": operation_type,
            "selected_price": max_price
        }
    )

# Управление категориями (список)
@app.get("/web/categories", response_class=HTMLResponse)
async def categories_page(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/web/login", status_code=303)
    
    categories = db.query(models.PlateCategory).all()
    return templates.TemplateResponse(
        "categories.html",
        {"request": request, "user": user, "categories": categories}
    )

# Добавление категории
@app.post("/web/add-category", response_class=HTMLResponse)
async def add_category(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    hardness_range: str = Form(...),
    db: Session = Depends(get_db)
):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/web/login", status_code=303)
    
    # Проверка на дубликат
    existing = db.query(models.PlateCategory).filter(models.PlateCategory.name == name).first()
    if existing:
        categories = db.query(models.PlateCategory).all()
        return templates.TemplateResponse(
            "categories.html",
            {
                "request": request, 
                "user": user, 
                "categories": categories,
                "error": "Категория с таким названием уже существует"
            }
        )
    
    category = models.PlateCategory(
        name=name,
        description=description,
        hardness_range=hardness_range
    )
    db.add(category)
    db.commit()
    
    return RedirectResponse(url="/web/categories", status_code=303)

# Удаление категории
@app.get("/web/delete-category/{category_id}")
async def delete_category(category_id: int, request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/web/login", status_code=303)
    
    # Проверка, есть ли пластины в этой категории
    plates_count = db.query(models.CuttingPlate).filter(models.CuttingPlate.category_id == category_id).count()
    if plates_count > 0:
        categories = db.query(models.PlateCategory).all()
        return templates.TemplateResponse(
            "categories.html",
            {
                "request": request, 
                "user": user, 
                "categories": categories,
                "error": f"Нельзя удалить категорию: в ней есть {plates_count} пластин"
            }
        )
    
    category = db.query(models.PlateCategory).filter(models.PlateCategory.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    
    return RedirectResponse(url="/web/categories", status_code=303)

# Информация о сервисе
@app.get("/api/info")
def api_info():
    return {
        "service": "Сервис подбора режущих пластин",
        "version": "1.0.0",
        "endpoints": {
            "web": {
                "home": "/",
                "login": "/web/login",
                "register": "/web/register",
                "dashboard": "/web/dashboard",
                "select": "/web/select-page",
                "categories": "/web/categories"
            },
            "api": {
                "auth": "/auth",
                "plates": "/plates",
                "select": "/select/plate"
            }
        }
    }

# Проверка здоровья
@app.get("/health")
def health_check():
    return {"status": "healthy"}